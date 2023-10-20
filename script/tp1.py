#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
from get_corpus import get_spacy_retok, get_conllu, test_tokens
from get_evaluation import get_tags, get_accuracy, get_precision, get_rappel, get_matrice

'''
    exemple de ce que l'on peut ecrire sur le terminal :
    python3 script/tp1.py -l zh -m lg
'''

parser = argparse.ArgumentParser()
parser.add_argument("-l", help="langue sur laquelle travailler : fr ou zh", default="fr")
parser.add_argument("-m", help="choix du modèle : sm, md, lg, trf", default="sm")
args = parser.parse_args()

# on récupère les corpus et les tags
corpus_r = get_conllu(args.l)
corpus_e = get_spacy_retok(args.l, args.m, corpus_r)
tags_e, tags_r = get_tags(corpus_e, corpus_r)

if corpus_e.nb_sentences == corpus_r.nb_sentences:
    
    acc = get_accuracy(corpus_r, corpus_e)
    print(f"L'accuracy est à {acc[0]}%.")
    print(f"En tenant compte du vocabulaire, l'accuracy est à {acc[1]}%.\n")
    # test_tokens(corpus_e, corpus_r)

    if acc != 100: # pas besoin de toute cela si l'accuracy est à 100%
        # on va regarder les catégories qu'ils classent le mieux
        for tag in tags_e:
            print(f"la precision pour {tag} est à {get_precision(corpus_e, corpus_r, tag)}%.")   
        for tag in set(tags_r):
            print(f"le rappel pour {tag} est à {get_rappel(corpus_e, corpus_r, tag)}%.")
        
        # on affiche ensuite les matrices de confusion
        get_matrice(corpus_e, corpus_r)
    
else :
    # si les corpus n'ont pas le même nombre de phrase, cela ne sert à rien de continuer
    print(f"\nLe corpus de reference a {corpus_r.number_sentences} phrases, et le corpus à evaluer {corpus_e.number_sentences}.")