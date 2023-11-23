#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Spacy prend les tag XPOS et non UPOS pour le training du modèle chinois, alors on remplace les XPOS par des UPOS
J'ai utilisé ce script pour les trois fichiers du corpus chinois
Les anciens fichiers se trouve dans le dossier ./oldcorpus/
"""

import regex

with open("./oldcorpus/lzh_kyoto-ud-dev.conllu", "r", encoding="utf-8") as file:
            data = file.readlines()
            
for line in data :
    line = regex.sub(r"(^.*\t.*\t.*\t)(.*\t)(.*\t)(.*\t.*\t.*\t.*\t.*)", r"\1\2\2\4", line)
    print(line, end="")