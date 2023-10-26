#!/bin/python3

# Objectif: couper le corpus en 4 sous-corpus.
# Paramètres: le corpus à couper
# Les noms des sous-corpus contenus dans sent_id qui servent de découpage

import sys
from pathlib import Path
import regex
#import os.path
from typing import List
from collections import defaultdict

def main(path: Path):
    read_conll(path)

def read_conll(path: Path):
    with open(path) as f:
        contenu_new_fichiers: defaultdict(str) = defaultdict(str)
        nouvelle_phrase: str = ""
        premiere_ligne: str = f.readline()
        sent_id: str = ""
        for line in f:
            line = line.strip()
            nouvelle_phrase += line + "\n"
            if line.startswith("# sent_id = "):
                sent_id = line[12:]
                corp_id = regex.findall(r'^\w+',sent_id)[0]
            elif line == "":
                contenu_new_fichiers[corp_id] += nouvelle_phrase
                nouvelle_phrase = ""
        for c in contenu_new_fichiers:
            with open(''.join(path.split('.')[:-1]) + '-' + c + ".conllu", 'w') as f:
                f.write(premiere_ligne)
                f.write(contenu_new_fichiers[c])

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Il manque le corpus.")
		sys.exit(1)
	path = sys.argv[1]
	main(path)
