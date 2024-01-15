#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    $ python evaluations/evaluate_jiayan.py

    Ce fichier compare la tokenisation du modèle jiayan 
    et de notre modèle que l'on a entrainé avec une tokenisation de référence
"""

from get_corpus import get_conllu, get_jiayan
from get_evaluation_jiayan import jiayan, jiayan_tc, test_tokens
    
    
def main():
    
    models = {
        "corpus_jiayan" : ("./models/jiayan/modele_jiayan", "BLUE"),
        "corpus_sentence" : ("./models/jiayan/modele_sentence", "YELLOW"),
        "corpus_table" : ("./models/jiayan/modele_table", "GREEN"),
        "corpus_word" : ("./models/jiayan/modele_word", "RED")
        }
    
    ## Partie 1. le modèle de référence
    # on récupère le vocabulaire
    corpus_train = get_conllu("train")
    vocabulaire = {token.form for sentence in corpus_train.sentences for token in sentence.tokens}
    # 'corpus_r' est le corpus de référence
    corpus_r = get_conllu("test", vocabulaire)
    
    ## Partie 2. les modèles jiayan
    # 'corpora' est une liste contenant les résultats des 4 modèles
    corpora = []
    for (title, (model, color)) in sorted(models.items()):
        corpora.append(get_jiayan(corpus_r, title, model, color))

    ## Partie 3. évaluation
    for i, corpus in enumerate(corpora):
        if i == 0:
            jiayan_tc(corpus, corpus_r)
        else:
            jiayan(corpus, corpus_r)
    
if __name__ == "__main__":
    main()