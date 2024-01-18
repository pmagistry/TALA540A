#!usr/bin/python
#*-* encoding : utf-8 *-*

from typing import List, Union, Dict, Set, Optional, Tuple
from dataclasses import dataclass
import os.path
from os import path
import subprocess
import codecs
import shutil
from pathlib import Path
import re
from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy
import itertools
from tqdm import tqdm

from pyJoules.energy_meter import measure_energy
from sklearn.metrics import classification_report

@dataclass
class Token:
	form: str
	tag: str
	is_oov: bool

@dataclass
class Sentence:
	sent_id: str # sent_id = annodis.er_00014 : variable "sid"
	tokens: List[Token]

@dataclass
class Corpus:
	sentences: List[Sentence]

def xml_to_conll(nom_fichier_xml:str, nom_fichier_out) -> str:
	"""
		prend un fichier .xml 
		retourne un fichier au format conllu
	"""
	regx_n = re.compile('(?<=<s n=")\d{4}+(?=">)')
	regx_tok = re.compile('(?<=>)[^ \n\t]+?(?=</)')
	regx_pos = re.compile('(?<=<).+?POS="(.+?)"(?=>)') # pos : group(1)
	with open(nom_fichier_xml) as file_xml, open('./character_conllu/'+nom_fichier_out+'.conllu', 'a') as file_conllu:
		for line in file_xml:
			result=""
			line = line.strip()
			if line.startswith('<file ID='):
				result += '\n# ' + line[1:14]
				print(result)
				file_conllu.write(result)
			cpteur_li = 0
			if line.startswith('<s n='):
				n = re.findall(regx_n, line)
				t = re.findall(regx_tok, line)
				p = re.findall(regx_pos, line)
				result += '\n'+'# sent_id'+n[0]+'\n'
				result += "# text = "+ "".join([tok for tok in t])+'\n'
				for tok, pos in zip(t, p):
					cpteur_li += 1
					result += "\t".join([str(cpteur_li),tok, "_", pos, "_", "_", "_", "_", "_", "_"]) + "\n"
				file_conllu.write(result)
# 				print(result)
		return
					
def read_conll(path:Path, vocabulaire: Optional[Set[str]] = None) -> Corpus:
	"""
	entrée : chemin de fichier, un ensemble vocab
	Lit un fichier au format connell et en extrait les formes et les POS pour chaque phrase.
	Extrait également le nom du sous-corpus.
	Remplit les champs sentences d'un dataclass Corpus avec les tokens (dataclass Token) 
	pour chaque phrase (dataclass Sentence).
	Si le vocabulaire n'est pas dans les arguments, le champ is_oov de Token est à True.
	sortie : un dataclass Corpus
	"""
	sentences: List[Sentence] = []
	tokens: List[Token] = []
	sid = ""
	with open(path) as f:
		for line in f:
			line = line.strip()
			if line.startswith("# file ID="):
				sid = line.split('"')[-2][0]
			if not line.startswith("#"):
				if line == "":
					sentences.append(Sentence(sent_id = sid, tokens = tokens))
					tokens = []
				else:
					fields = line.split("\t")
					form, tag = fields[1], fields[3]
					if vocabulaire is None:
						is_oov = True
					else:
						is_oov = not form in vocabulaire
					tokens.append(Token(form, tag, is_oov))
	return Corpus(sentences)

def build_vocabulaire(corpus: Corpus) -> Set[str]:
	"""
		entrée : un dataclass Corpus
		Extrait le vocabulaire (set) des champs tokens d'un dataclass Corpus.
		Il servira à savoir si un token est un oov lors de l'appel de read_cnll()
		sortie : un ensemble de strings de tokens vocabulaire 
	"""
	return {tok.form for sent in corpus.sentences for tok in sent.tokens}
	
def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
	"""
		entrée : champs sentences d'un dataclass
		Crée un SpacyDoc à partir des champs sentences du dataclass Corpus gold.
		avec le vocabulaire du SpacyDoc à partir des tok.form du dataclass Corpus gold.
		sortie : SpacyDoc
	"""
	words = [tok.form for tok in sentence.tokens]
	return SpacyDoc(vocab, words = words)

def doc_to_sentence(doc: SpacyDoc, origin: Sentence) -> Sentence:
	"""
		entrée : un SpacyDoc, un dataclass Sentence du corpus d'origine
		Crée des sentences à partir d'un objet SpacyDoc
		À partir des Sentence (List[Token]) d'un Corpus (gold)
		Crée de nouveaux Sentence auxquelles ajoute les tok.pos_ du modèle Spacy.
		sortie : un dataclass Sentence
	"""
	tokens = []
	for tok, origin_token in zip(doc, origin.tokens):
		tag = tok.pos_
		if len(tag) == 0:
			tag = tok.tag_
		tokens.append(Token(tok.text, tag, is_oov = origin_token.is_oov))
	return Sentence(origin.sent_id, tokens)
	
#@measure_energy
def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline, nom_do:str) -> Corpus:
	"""
		entrée : un dataclass Corpus, un modèle Spacy
		Crée le corpus test (objet Corpus) à partir des tok.form du corpus gold 
		avec les tok.tag_ du modèle Spacy.
		sortie : un dataclass Corpus
	"""
	sentences = []
	for sentence in corpus.sentences:
		doc = sentence_to_doc(sentence, model_spacy.vocab)
		doc = model_spacy(doc)
		sentences.append(doc_to_sentence(doc, sentence))
		for S in sentences:
			S.sent_id = nom_do
	return Corpus(sentences)

def sentence_to_conll(sent: Sentence) -> str:
	"""
		prend un dataclass Sentence d'un dataclass Corpus
		retourne : une string par phrase et une string par token au format conllu
	"""
	result = f"\n# sent_id = {sent.sent_id}\n"
	text = " ".join([tok.form for tok in sent.tokens])
	result += f"# text = {text}\n"
	for i, token in enumerate(sent.tokens):
		result += "\t".join([str(i+1), token.form, "_", token.tag, "_", "_", "_", "_", "_", "_"]) + "\n"
	return result	

def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus, subcorpus: Optional[str] = None) -> Tuple[float, float]:
	"""
		entrée : un dataclass corpus gold et un test, le nom d'un sous-corpus (optionel)
		Calcule l'exactitude en itérant sur les sentences des corpus gold et test et en comparant les étiquettes de POS.
		Si étiquettes sont les mêmes cpteur ok incrémenté
		Incrémentation d'un cpteur pour les tags des oov du corpus gold par rapport à ceux du test.
		Incrémentation d'un cpteur total pour les tags et les oov.
		sortie : les proportions de tags ok sur les totaux : 
		- pour le tokens originaux 
		- pour les oov
	"""
	nb_ok = 0
	nb_total = 0
	oov_ok = 0
	oov_total = 0
	for sentence_gold, sentence_test in zip(
		corpus_gold.sentences, corpus_test.sentences
	):
		if subcorpus is None or subcorpus in sentence_gold.sent_id:
			for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
				assert token_gold.form == token_test.form
				if token_gold.tag == token_test.tag:
					nb_ok += 1
				nb_total += 1
				if token_gold.is_oov:
					oov_total += 1
					if token_gold.tag == token_test.tag:
						oov_ok += 1
	return nb_ok / nb_total, oov_ok / oov_total

def print_report(corpus_gold: Corpus, corpus_test: Corpus):
	ref = [tok.tag for sent in corpus_test.sentences for tok in sent.tokens]
	test = [tok.tag for sent in corpus_gold.sentences for tok in sent.tokens]
	return classification_report(ref, test)

if __name__=="__main__":

# Création des répertoires
	if path.isdir('./character_conllu/') == False:
		subprocess.check_output(['mkdir', './character_conllu/'])
	if path.isdir('./sous_corpus_conllu/') == False:
		subprocess.check_output(['mkdir', './sous_corpus_conllu/'])
	if path.isdir('./ss_corps_cnll_spacy_tags/') == False:
		subprocess.check_output(['mkdir', './ss_corps_cnll_spacy_tags/'])
	if path.isdir('./sous_corpus_test/') == False:
		subprocess.check_output(['mkdir', './sous_corpus_test/'])
	if path.isdir('./sous_corpus_train/') == False:
		subprocess.check_output(['mkdir', './sous_corpus_train/'])
	if path.isdir('./sous_corpus_dev/') == False:
		subprocess.check_output(['mkdir', './sous_corpus_dev/'])
	if path.isdir('./spacy_sous_corpus/') == False:
		subprocess.check_output(['mkdir', './spacy_sous_corpus/'])
	if path.isdir('./spacy_sous_corpus/train') == False:
		subprocess.check_output(['mkdir', './spacy_sous_corpus/train'])
	if path.isdir('./spacy_sous_corpus/dev') == False:
		subprocess.check_output(['mkdir', './spacy_sous_corpus/dev'])
	if path.isdir('./spacy_sous_corpus/test') == False:
		subprocess.check_output(['mkdir', './spacy_sous_corpus/test'])
	if path.isdir('./spacy_model_ss_corps/') == False:
		subprocess.check_output(['mkdir', './spacy_model_ss_corps/'])
	if path.isdir('./spacy_model_ss_corps/non_divers') == False:
		subprocess.check_output(['mkdir', './spacy_model_ss_corps/non_divers'])
	if path.isdir('./spacy_model_ss_corps/non_essais') == False:
		subprocess.check_output(['mkdir', './spacy_model_ss_corps/non_essais'])
	if path.isdir('./spacy_model_ss_corps/non_fiction') == False:
		subprocess.check_output(['mkdir', './spacy_model_ss_corps/non_fiction'])
	if path.isdir('./spacy_model_ss_corps/non_news') == False:
		subprocess.check_output(['mkdir', './spacy_model_ss_corps/non_news'])
	if path.isdir('./spacy_model_ss_corps/non_populaire') == False:
		subprocess.check_output(['mkdir', './spacy_model_ss_corps/non_populaire'])
	if path.isdir('./spacy_model_ss_corps/non_religion') == False:
		subprocess.check_output(['mkdir', './spacy_model_ss_corps/non_religion'])
	if path.isdir('./spacy_model_ss_corps/non_sci_aca') == False:
		subprocess.check_output(['mkdir', './spacy_model_ss_corps/non_sci_aca'])
	
# 	conversion des fichiers xml au format conllu
	chemin = Path('./character')
	for f_xml in sorted(list(chemin.iterdir())):
		nom_fichier = str(f_xml).split('/')[-1].split('.')[0]
		xml_to_conll(f_xml, nom_fichier)
		
	# concaténation des fichiers conllu de sous-corpus par domaines
	# on a 7 domaines
	dico_domaines = {'news':['LCMC_A', 'LCMC_B', 'LCMC_C'], 'religion':['LCMC_D'], 'populaire':['LCMC_E', 'LCMC_F', 'LCMC_R'], 'essais':['LCMC_G'], 'divers':['LCMC_H'], 'sci_aca':['LCMC_J'], 'fiction':['LCMC_K', 'LCMC_M', 'LCMC_N', 'LCMC_P']}
	for k, v in dico_domaines.items():
		with codecs.open(f'./sous_corpus_conllu/LCMC_{k}.conllu','wb', encoding='utf8') as file_out:
			for val in v:
				with codecs.open(f'./character_conllu/{val}.conllu','rb', encoding='utf8') as file_in:
					shutil.copyfileobj(file_in, file_out)
	
	corpus_set = {'news', 'religion',  'populaire', 'essais', 'divers', 'sci_aca', 'fiction'}
	k = len(corpus_set)-1
	sous_corpus_list = list(itertools.combinations(corpus_set, k))

# création des dataclass : un par domaine étiqueté avec Spacy et avec les id de domaines
# écriture du fichier sous-corpus .conllu avec les tags Spacy qui sera le corpus de test
	chemin = Path('./sous_corpus_conllu/')
	file_list = sorted(list(chemin.iterdir()))

	model_spacy = spacy.load("zh_core_web_sm")
	
# 	Préparation des corpus_test : un par domaine (sous-corpus)
	for f in tqdm(file_list):
		if not f.name.endswith('.DS_Store'):
			nom_do = f.name.split('.')[0][5:]
			c_dataclass = read_conll(f)
			corpus_spacy = tag_corpus_spacy(c_dataclass, model_spacy, nom_do)
			with open(f'./sous_corpus_test/sous_corpus_test_{nom_do}.conllu', 'w') as file_out:
				for s in corpus_spacy.sentences:
					if s.tokens != []:
						file_out.write(sentence_to_conll(s))
	 
# le découpage des corpus dev et train est fait à la ligne de commande

# 	concaténation des .conllu train hors domaine, le nom du fichier est celui du domaine manquant
	for e in sous_corpus_list:
		ens = set([e2 for e2 in e])
		do_manquant = "".join(corpus_set.difference(ens))
		with open(f'./sous_corpus_train/sous_corpus_train_{do_manquant}.conllu', 'a') as file_out:
			for f in e:
				with open(f'./ss_corps_cnll_spacy_tags/train/sous_corpus_train_{f}.conllu', 'r') as file_in:
					file_out.write('\n')
					file_out.write(file_in.read())		
			
#  concaténation des .conllu dev hors domaine, le nom du fichier est celui du domaine manquant
		for e in sous_corpus_list:
		ens = set([e2 for e2 in e])
		do_manquant = "".join(corpus_set.difference(ens))
		with open(f'./sous_corpus_dev/sous_corpus_dev_{do_manquant}.conllu', 'a') as file_out:
			for f in e:
				with open(f'./ss_corps_cnll_spacy_tags/dev/sous_corpus_dev_{f}.conllu', 'r') as file_in:
					file_out.write('\n')
					file_out.write(file_in.read())
	
# on convertit les corpus .conllu en corpus .spacy à la ligne de commande
	
#  	Entraînement du modèle à la ligne de commande on garde le même que pour le tagging "zh_core_web_sm"
#  	chaque fois avec le train et dev au nom du domaine manquant
 	
#  le train est toujours le .conllu qui a été utilisé pour l'entraînement du modèle. 
# 	Pour avoir le vocabulaire des domaines sauf celui du domaine testé
	corpus_train = read_conll("./sous_corpus_train/sous_corpus_train_divers.conllu")
	vocab_train = build_vocabulaire(corpus_train)

# 	for model_name in ("./spacy_model_ss_corps/non_annodis/model-best"):
	model_name = "./spacy_model_core_web_sm/non_divers/model-best"
	model_spacy = spacy.load(model_name)
	corpus_gold = read_conll("./sous_corpus_test/sous_corpus_test_divers.conllu", vocabulaire = vocab_train)
	corpus_test = tag_corpus_spacy(corpus_gold, model_spacy, 'divers')
	with open('resultats_eval_sous_corpus.txt', 'a') as file_out:
		print(model_name)
		file_out.write(model_name+'\n') 
		print(compute_accuracy(corpus_gold, corpus_test))
		file_out.write(str(compute_accuracy(corpus_gold, corpus_test))+'\n')
		print(print_report(corpus_gold, corpus_test))
		file_out.write(print_report(corpus_gold, corpus_test)+'\n')		
 	