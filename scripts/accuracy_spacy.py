#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datastructures_corpus import Corpus, Phrase, Token
from pprint import pprint
import sys, spacy


def make_corpus_conll(file:str):
	with open(file, "r") as f:
		content=f.read()
		# Initialisation d'une instance de Corpus
		corpus=Corpus([])
		# Création d'une liste où chaque élément est une phrase (métadonnées + analyse)
		sents=content.split("\n\n")
		for i in range(len(sents)-1):
			# Initialisation phrase
			sentence=Phrase("", "", [])
			# On a une liste d'éléments par phrase (metadata + analyse Token)
			sent_data=sents[i].split("\n")
			meta=[]
			for data in sent_data:
				# Les metadata commencent par un #
				if data.startswith("#"):
					meta.append(data)
					# Initialisation d'une instance de Phrase
					for d in meta : 
						if "sent_id" in d:
							sentence.sent_id=d.split(" = ")[1]
						if "text" in d:
							sentence.text=d.split(" = ")[1]
				else:
					token_ana=data.split("\t")
					# Permet de faire correspondre à chaque élément de la liste l'attribut associé en fonction de l'ordre/indice
					tok=Token(*token_ana)
					# éviter les contractions type "du"
					if not "-" in token_ana[0]:
						sentence.analyse.append(tok)
			corpus.liste_sent.append(sentence)
	return corpus

def make_corpus_spacy(corpus_gold : Corpus, spacy_model) -> Corpus :
	corpus_spacy=Corpus([])
	nlp=spacy.load(spacy_model)
	for sent in corpus_gold.liste_sent:
		sent_spacy=Phrase("","",[])
		doc=nlp(sent.text)
		sent_spacy.text=sent.text
		sent_spacy.sent_id=sent.sent_id
		compt=1
		for tok in doc:
			tok_spacy=Token(compt, tok.text, tok.lemma_, tok.pos_, tok.tag_, "", "", "", "", "")
			compt+=1
			sent_spacy.analyse.append(tok_spacy)
		corpus_spacy.liste_sent.append(sent_spacy)
	return corpus_spacy


def compar_listes(corpus_gold : Corpus, corpus_test : Corpus):
	compt_true=0
	compt_tot=0
	for sent_gold, sent_test in zip(corpus_gold.liste_sent, corpus_test.liste_sent):
		for token_gold, token_test in zip(sent_gold.analyse, sent_test.analyse):
			assert(token_gold.forme == token_test.forme)
			if token_gold.upos == token_test.upos:
				compt_true += 1
			compt_tot += 1
	return compt_true / compt_tot

if __name__=="__main__":
	corpus=sys.argv[1]
	model=sys.argv[2]
	c_gold=make_corpus_conll(corpus)
	c_test=make_corpus_spacy(c_gold, model)
	acc=compar_listes(c_gold, c_test)
	print(f"L'accuracy moyenne du modèle {model} de spacy sur ce corpus est de : {acc}")
