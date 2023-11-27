#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    $ python evaluations/evaluate_jiayan.py

    Ce fichier compare la tokenisation du modèle jiayan 
    et de notre modèle que l'on a entrainé avec une tokenisation de référence
"""

from get_corpus import get_conllu, get_jiayan
from get_evaluation_jiayan import jiayan_sans, test_tokens
    
    
def main():
    
    ## Partie 1. le modèle de référence
    # on récupère le vocabulaire
    corpus_train = get_conllu("train")
    vocabulaire = {token.form for sentence in corpus_train.sentences for token in sentence.tokens}
    # 'corpus_r' est le corpus de référence
    corpus_r = get_conllu("test", vocabulaire)
    
    ## Partie 2. le modèle jiayan
    # 'models_jiayan' est un dictionnaire des noms des modèles spacy
    models = {
        "corpus_jiayan" : ("./models/jiayan/original_pos_model", "BLUE") # reste BLACK
        }
    # 'corpora' est une liste contenant les résultats des 5 modèles
    corpora = []   
    for (title, (model, color)) in sorted(models.items()):
        corpora.append(get_jiayan(corpus_r, title, model, color))
    # test_tokens(corpora[0], corpus_r)
    
    ## Partie 3. évaluation avec subcorpus
    
    ## Partie 4. évaluation sans subcorpus
    for corpus in corpora :
        jiayan_sans(corpus, corpus_r)
    
if __name__ == "__main__":
    main()