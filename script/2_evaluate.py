#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    python ./script/2_evaluate.py

Ce fichier compare la tokenisation des modèles spacy et de notre modèle que l'on a entrainé avec une tokenisation de référence
"""

from get_corpus import get_conllu, get_vocab, get_spacy
from get_evaluation import get_accuracy, get_matrice, test_tokens
import sys


################ partie 1. le modèle de référence ################

# on récupère le vocabulaire
corpus_train = get_conllu("train")
vocabulaire = get_vocab(corpus_train)

# 'corpus_r' est le corpus de référence
corpus_r = get_conllu("test", vocabulaire)


######### partie 1b. pour test avec modèle spacy au choix #########

# corpus_e = get_spacy(corpus_r, "mon_modele", "./script/model_spacy/monmodel/model-best", "YELLOW")
# test_tokens(corpus_e, corpus_r)
# sys.exit(0)


#################### partie 2. les modèles spacy ####################

# 'models' est un dictionnaire des noms des modèles spacy
models = {
    "corpus_lg" : ("zh_core_web_lg", "GREEN"),
    "corpus_md" : ("zh_core_web_md", "CYAN"),
    "corpus_sm" : ("zh_core_web_sm", "MAGENTA"),
    "corpus_trf" : ("zh_core_web_trf", "RED"),
    "mon_modele" : ("./script/model_spacy/monmodel/model-best", "YELLOW")
}

# 'corpora' est une liste contenant les résultats des 4 modèles
corpora = []
    
# petite boucle pour faire marcher chaque modèle
for (title, (model, color)) in sorted(models.items()):   
    corpora.append(get_spacy(corpus_r, title, model, color))

# 'corpus_lg', corpus_md', 'corpus_sm', 'corpus_trf' sont les corpus spacy
# 'corpus_e' est le corpus de notre modèle
corpus_lg, corpus_md, corpus_sm, corpus_trf, corpus_e = (corpus for corpus in corpora)
# test_tokens(corpus_e, corpus_r)


################# partie 3. évaluation avec subcorpus #################

for subcorpus in {sentence.sent_id for sentence in corpus_r.sentences}:   
    print(f"\nPour le sous-corpus {subcorpus} :")         
    acc_e = get_accuracy(corpus_e, corpus_r, subcorpus)
    print(f"L'accuracy avec notre modèle est à {acc_e[0]}%.")
    print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_e[1]}%.")
    print("La matrice de confusion, sans tenir compte du vocabulaire")
    get_matrice(corpus_e, corpus_r, subcorpus)
    

################# partie 4. évaluation sans subcorpus #################

acc_e = get_accuracy(corpus_e, corpus_r)
print(f"L'accuracy avec notre modèle est à {acc_e[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_e[1]}%.")
print("La matrice de confusion, sans tenir compte du vocabulaire")
get_matrice(corpus_e, corpus_r)

acc_trf = get_accuracy(corpus_trf, corpus_r)
print(f"\nL'accuracy avec le modèle spacy trf est à {acc_trf[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_trf[1]}%.")
print("La matrice de confusion, sans tenir compte du vocabulaire")
get_matrice(corpus_trf, corpus_r)

acc_lg = get_accuracy(corpus_lg, corpus_r)
print(f"\nL'accuracy avec le modèle spacy lg est à {acc_lg[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_lg[1]}%.")
print("La matrice de confusion, sans tenir compte du vocabulaire")
get_matrice(corpus_lg, corpus_r)

acc_md = get_accuracy(corpus_md, corpus_r)
print(f"\n'accuracy avec le modèle spacy md est à {acc_md[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_md[1]}%.")
print("La matrice de confusion, sans tenir compte du vocabulaire")
get_matrice(corpus_md, corpus_r)

acc_sm = get_accuracy(corpus_sm, corpus_r)
print(f"\nL'accuracy avec le modèle spacy sm est à {acc_sm[0]}%.")
print(f"En tenant compte du vocabulaire, l'accuracy est à {acc_sm[1]}%.")
print("La matrice de confusion, sans tenir compte du vocabulaire")
get_matrice(corpus_sm, corpus_r)
