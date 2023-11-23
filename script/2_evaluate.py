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
from datastructures import Corpus


def avec_souscorpus(corpus: Corpus, rcorpus: Corpus) :
    print(f"\nPour le corpus {corpus.name} :")
    for subcorpus in {sentence.sent_id for sentence in rcorpus.sentences}:   
        print(f"Pour le sous-corpus {subcorpus} :")         
        acc = get_accuracy(corpus, rcorpus, subcorpus)
        print(f"L'accuracy avec notre modèle est à {acc[0]}%.")
        print(f"En tenant compte du vocabulaire, l'accuracy est à {acc[1]}%.")
        print("La matrice de confusion, sans tenir compte du vocabulaire")
        get_matrice(corpus, rcorpus, subcorpus)
    
    
def sans_soucorpus(corpus: Corpus, rcorpus: Corpus) :
    print(f"\nPour le corpus {corpus.name} :")
    acc = get_accuracy(corpus, rcorpus)
    print(f"L'accuracy avec notre modèle est à {acc[0]}%.")
    print(f"En tenant compte du vocabulaire, l'accuracy est à {acc[1]}%.")
    print("La matrice de confusion, sans tenir compte du vocabulaire")
    get_matrice(corpus, rcorpus)
    
    
def main():
    
    ## Partie 1. le modèle de référence
    # on récupère le vocabulaire
    corpus_train = get_conllu("train")
    vocabulaire = get_vocab(corpus_train)
    # 'corpus_r' est le corpus de référence
    corpus_r = get_conllu("test", vocabulaire)

    ## Partie 2. les modèles spacy
    # 'models' est un dictionnaire des noms des modèles spacy
    models = {
        "corpus_lg" : ("zh_core_web_lg", "GREEN"),
        "corpus_md" : ("zh_core_web_md", "CYAN"),
        "corpus_sm" : ("zh_core_web_sm", "MAGENTA"),
        "corpus_trf" : ("zh_core_web_trf", "RED"),
        "mon_modele" : ("./script/model_spacy/monmodel/model-best", "YELLOW")
        }
    # 'corpora' est une liste contenant les résultats des 5 modèles
    corpora = []
    for (title, (model, color)) in sorted(models.items()):   
        corpora.append(get_spacy(corpus_r, title, model, color))
    # test_tokens(corpora[4], corpus_r) # pour tester un des corpus

    ## Partie 3. évaluation avec subcorpus
    # 'corpora[4]' est le corpus de notre modèle
    avec_souscorpus(corpora[4], corpus_r)
        
    ## Partie 4. évaluation sans subcorpus
    for corpus in corpora :
        sans_soucorpus(corpus, corpus_r)


if __name__ == "__main__":
    main()