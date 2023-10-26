#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    python3 script/tp2.py -l fr

Ce fichier compare la tokenisation du modèle spacy que l'on a entrainé avec une tokenisation de référence
"""

import argparse
from get_spacy import get_spacy_mymodel, get_spacy
from get_conllu import get_conllu, get_vocab
from get_evaluation import get_accuracy, get_matrice, test_tokens


parser = argparse.ArgumentParser()
parser.add_argument(
    "-l", help="langue sur laquelle travailler : fr ou zh", default="fr"
)
args = parser.parse_args()


if args.l == "zh" :
    corpus_train = get_conllu(args.l, "train")
    vocabulaire = get_vocab(corpus_train)
else :
    corpus_train = get_conllu(args.l, "train")
    vocabulaire = get_vocab(corpus_train)

# 'corpus_r' est le corpus de référence
corpus_r = get_conllu(args.l, "test", vocabulaire)
# 'corpus_e' est le corpus de notre modèle
corpus_e = get_spacy_mymodel(args.l, corpus_r)
# test_tokens(corpus_e, corpus_r)

# # 'corpus_lg', 'corpus_md', 'corpus_sm' sont les corpus spacy
corpus_lg, corpus_md, corpus_sm = get_spacy(args.l, corpus_r)


# on affiche l'accuracy et la matrice de confusion
acc_e = get_accuracy(corpus_e, corpus_r)
print(f"\nL'accuracy avec notre modèle est à {acc_e[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_e[1]}%.")
get_matrice(corpus_e, corpus_r, args.l)


acc_lg = get_accuracy(corpus_lg, corpus_r)
print(f"\nL'accuracy avec le modèle spacy lg est à {acc_lg[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_lg[1]}%.")
get_matrice(corpus_lg, corpus_r, args.l)


acc_md = get_accuracy(corpus_md, corpus_r)
print(f"\n'accuracy avec le modèle spacy md est à {acc_md[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_md[1]}%.")
get_matrice(corpus_md, corpus_r, args.l)


acc_sm = get_accuracy(corpus_sm, corpus_r)
print(f"\nL'accuracy avec le modèle spacy sm est à {acc_sm[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_sm[1]}%.")
get_matrice(corpus_sm, corpus_r, args.l)