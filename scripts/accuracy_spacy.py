#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datastructures_corpus import Corpus, Phrase, Token
from pprint import pprint
import sys, spacy



def make_corpus(file:str):
	with open(file, "r") as f:
		content=f.read()
		# Initialisation d'une instance de Corpus
		corpus=Corpus([])
		# Création d'une liste où chaque élément est une phrase (métadonnées + analyse)
		sents=content.split("\n\n")
		for i in range(len(sents)-1):
			sent_data=sents[i].split("\n")
			# Les 3 premières lignes de chaque phrase correspondent aux metadata
			meta=[data.split("=")[1] for data in sent_data[:3]]
			# Initialisation d'une instance de Phrase
			sentence=Phrase(meta[0].strip(), meta[1].strip(), meta[2].strip(), [])

			for token in sent_data[3:]:
				token_ana=token.split("\t")
				# Permet de faire correspondre à chaque élément de la liste l'attribut associé en fonction de l'ordre/indice
				tok=Token(*token_ana)
				sentence.analyse.append(tok)
			corpus.liste_sent.append(sentence)
	return corpus

def compar_listes(liste_1 : list, liste_2 : list):
	compt_false=0
	compt_true=0
	min_length=min(len(pos_list_corp), len(pos_list_spacy))
	for i in range(min_length):
		if pos_list_corp[i]==pos_list_spacy[i]:
			compt_true+=1
		else:
			compt_false+=1
	if len(liste_1) > min_length:
		compt_false += len(liste_1)-min_length
	elif len(liste_2) > min_length:
		compt_false += len(liste_2)-min_length
	return compt_true, compt_false

if __name__=="__main__":
	corpus=sys.argv[1]
	nlp=spacy.load("ko_core_news_md")
	c=make_corpus(corpus)
	dico_acc={}
	sum_acc=0
	for phrase in c.liste_sent:
		doc=nlp(phrase.text)
		pos_list_spacy=[token.pos_ for token in doc]
		pos_list_corp=[tok.upos for tok in phrase.analyse]
		true, false = compar_listes(pos_list_corp, pos_list_spacy)
		acc=true/(true + false)
		dico_acc.update({phrase.sent_id:acc})
		sum_acc+=acc
	moy_acc=sum_acc/len(c.liste_sent)
	print(f"L'accuracy moyenne de spacy sur ce corpus est de : {moy_acc}")
