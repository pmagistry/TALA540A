#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# Valentina Osetrov

import spacy
import conllu

def token_pos_txt(fic_txt_path):
    """
    Retourne les tokens et les POS d'un fichier txt
    """
    nlp = spacy.load("fr_core_news_sm")

    # Ouvrir le fichier
    with open(fic_txt_path, "r") as ftxt:
        texte = ftxt.read()

    doc = nlp(texte)

    # Initialiser des listes vides pour stocker les tokens et leurs POS
    tokens_txt = []
    pos_txt = []

    # Parcourir les tokens et extraire les formes avec leurs POS
    for token in doc:
        tokens_txt.append(token.text)
        pos_txt.append(token.pos_)

    return tokens_txt, pos_txt

# Appeler la fonction
fic_txt_path = "texte_brut.txt"
tokens_txt, pos_txt = token_pos_txt(fic_txt_path)


def token_pos_conllu(fic_conllu_path):
    """
    Retourne les tokens et les POS d'un fichier conllu
    """
    # Ouvrir le fichier
    with open(fic_conllu_path, 'r') as fconllu:
        donnees = fconllu.read()

    # Analyser les données
    analyse = conllu.parse(donnees)

    # Initialiser des listes vides pour stocker les tokens et leurs POS
    tokens_conllu = []
    pos_conllu = []

    # Parcourir les tokens et extraire les formes avec leurs POS
    for i in analyse:
        for token in i:
            form = token['form']
            upos = token['upostag']
            tokens_conllu.append(form)
            pos_conllu.append(upos)

    return tokens_conllu, pos_conllu

# Appeler la fonction
fic_conllu_path = 'fr_sequoia-ud-test.conllu'
tokens_conllu, pos_conllu = token_pos_conllu(fic_conllu_path)

# Comparer les POS tags des deux fichiers
if len(pos_txt) != len(pos_conllu):
    print("Pas le même nombre de données !")
else:
    etre_identique = True  

    for i in range(len(pos_txt)):
        if pos_txt[i] != pos_conllu[i]:
            etre_identique = False
            print(f"Différence : txt POS à : {i} = {pos_txt[i]}, conllu POS à : {i} = {pos_conllu[i]}")