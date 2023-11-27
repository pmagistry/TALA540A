#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier corpus :
    python extract.py > path_nouveau_fichier

J'ai utilisé ce script pour modifier les fichiers conllu en fonction de mes besoins
Les anciens fichiers se trouve dans le dossier ./oldcorpus/
"""

import regex

with open("./lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as file:
    data = file.readlines()

for line in data:
    # line = regex.sub(r"(^.*\t.*\t.*\t)(.*\t)(.*\t)(.*\t.*\t.*\t.*\t.*)", r"\1\2\2\4", line)
    # print(line, end="")

    if not regex.match(r"^#", line) and not regex.match(r"^\n", line):
        line = regex.sub(r"^.*\t(.*\t).*\t(.*)\t.*\t.*\t.*\t.*\t.*\t.*$", r"\1\2", line)
        print(line, end="")
