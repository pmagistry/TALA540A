#!/usr/bin/env/python
# coding: UTF-8

from typing import List, Dict
import re
import os
from collections import defaultdict
import spacy
import spacy_udpipe
from spacy.tokens import Doc
from datastruct import Token

#Objectif : évaluer les résultats du modèle d'étiquetage de Spacy par rapport à l'étiquetage de Connell


def spacy_load(chemin, nom_fichier_txt):
	"""
		charge un fichier texte dans le moteur spacy
		renvoie un objet Doc : <class 'spacy.tokens.doc.Doc'>
	"""
	nlp = spacy.load("fr_core_news_sm")
	with open(chemin+nom_fichier_txt, 'r') as file:
		texte = file.read()
		texte=re.sub("\n", "", texte)
		nlp_doc = nlp(texte)
	return nlp_doc
	
def make_token_spacy(nlp_doc):
	token_list_spacy=[]
	for t in document:
		token = Token(t.text, t.lemma, t.pos_)
		token_list_spacy.append(token)
	return token_list_spacy

def make_token_cnll(cnll_texte):
	p = re.compile('[0-9]+\t(.+?)\t(.+?)\t(.+?)\t')
	token_list_cnll=[]
	with open (cnll_texte, 'r') as f:
		lines=f.readlines()
		texte=" ".join(lines)
		for m in re.finditer(p, texte):
			token = Token(m.group(1), m.group(2), m.group(3))
			token_list_cnll.append(token)
	return token_list_cnll
		
def compare_pos(liste_test, liste_ref):
	positifs=[]
	decal=0
	if len(liste_test)<len(liste_ref):
		print(f"décalage !\n liste_test : {len(liste_test)} tokens < liste_ref : {len(liste_ref)} tokens")
	for t1, t2 in zip(liste_test, liste_ref):
		positifs.append(t1 == t2)
	return sum(positifs), len(positifs), sum(positifs)/len(positifs)
			
	
if __name__ == "__main__":
	
	chemin = os. getcwd()+'/'
	nom_fichier_txt ="corpus_a_tester.txt"
	document = spacy_load(chemin, nom_fichier_txt)

	token_pos_list_spacy=[(t.forme, t.pos) for t in make_token_spacy(document)]
	print(len(token_pos_list_spacy))
	
	document_ref="fr_sequoia-ud-test.conllu"
	token_pos_list_cnll=[(t.forme, t.pos) for t in make_token_cnll(document_ref)]
	print(len(token_pos_list_cnll))

	res = compare_pos(token_pos_list_spacy, token_pos_list_cnll)
	print(f"nombre de tokens bien segmentés/étiquetés : {res[0]}\n \
			nombre total de tokens : {res[1]}, \n\
			pourcentage de tokens bien segmentés/étiquetés : {res[2]*100}")