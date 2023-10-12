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
			# Initialisation phrase
			sentence=Phrase("", "", "", [])
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
					sentence.analyse.append(tok)
			corpus.liste_sent.append(sentence)
	return corpus

def compar_listes(tokens_gold : list, tokens_test : list):
	compt_false=0
	compt_true=0
	min_length=min(len(tokens_gold), len(tokens_test))
	for i in range(min_length):
		if tokens_gold[i]==tokens_test[i]:
			compt_true+=1
		else:
			compt_false+=1
	if len(tokens_gold) > min_length:
		compt_false += len(tokens_gold)-min_length
	elif len(tokens_test) > min_length:
		compt_false += len(tokens_test)-min_length
	return compt_true, compt_false

if __name__=="__main__":
	corpus=sys.argv[1]
	model=sys.argv[2]
	nlp=spacy.load(model)
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
	print(f"L'accuracy moyenne du modèle {model} de spacy sur ce corpus est de : {moy_acc}")
