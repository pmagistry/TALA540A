#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier corpus :
    python extract.py > path_nouveau_fichier

J'ai utilisé ce script pour modifier les fichiers conllu en fonction de mes besoins
Les anciens fichiers se trouve dans le dossier ./oldcorpus/
"""

import regex
from conllu import parse

# with open("./lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as file:
#     data = file.readlines()

# for line in data:
#     # pour corpus conllu 
#     line = regex.sub(r"(^.*\t.*\t.*\t)(.*\t)(.*\t)(.*\t.*\t.*\t.*\t.*)", r"\1\2\2\4", line)
#     print(line, end="")
#     # pour corpus du premier module jiayan avec entrainement caractère par caractère
#     if not regex.match(r"^#", line) and not regex.match(r"^\n", line):
#         line = regex.sub(r"^.*\t(.*)\t.*\t(.*)\t.*\t.*\t.*\t.*\t.*\t.*$", r"\1\t\2", line)
#         print(line, end="")

# pour corpus du deuxième module jiayan avec entrainement phrase par phrase
with open("lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as f :
    tables = parse(f.read()) 

for table in tables:
    phrase = []
    tags = []
    for token in table:
        phrase.append(token["form"])
        tags.append(token["upos"])
    print(" ".join(phrase), "\t", " ".join(tags))