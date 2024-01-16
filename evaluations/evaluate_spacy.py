#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    $ python evaluations/evaluate_spacy.py

    Ce fichier compare la tokenisation des modèles spacy 
    et de notre modèle que l'on a entrainé avec une tokenisation de référence
"""

from get_corpus import get_conllu, get_spacy
from get_evaluation_spacy import spacy_avec, spacy_sans
    
    
def main():
    
    # models_spacy = {
    #     "corpus_lg" : ("zh_core_web_lg", "GREEN"),
    #     "corpus_md" : ("zh_core_web_md", "CYAN"),
    #     "corpus_sm" : ("zh_core_web_sm", "MAGENTA"),
    #     "corpus_trf" : ("zh_core_web_trf", "RED")
    #     }
    
    # my_models = {
    #     "corpus_1" : ("./models/spacy/modele1/model-best", "GREEN"),
    #     "corpus_2" : ("./models/spacy/modele2/model-best", "CYAN"),
    #     "corpus_3" : ("./models/spacy/modele3/model-best", "MAGENTA"),
    #     "corpus_4" : ("./models/spacy/modele4/model-best", "RED"),
    #     "corpus_5" : ("./models/spacy/modele5/model-best", "YELLOW")
    # }
    
    my_models = {
        "corpus_6" : ("./models/spacy/modele6/model-best", "GREEN"),
        "corpus_7" : ("./models/spacy/modele7/model-best", "CYAN"),
        "corpus_8" : ("./models/spacy/modele8/model-best", "MAGENTA"),
        "corpus_9" : ("./models/spacy/modele9/model-best", "RED"),
        "corpus_10" : ("./models/spacy/modele10/model-best", "YELLOW")
    }
    
    ## Partie 1. le modèle de référence
    # on récupère le vocabulaire
    corpus_train = get_conllu("train")
    vocabulaire = {token.form for sentence in corpus_train.sentences for token in sentence.tokens}
    # 'corpus_r' est le corpus de référence
    corpus_r = get_conllu("test", vocabulaire)

    ## Partie 2. les modèles spacy
    # 'corpora' est une liste contenant les résultats des modèles spacy
    corpora = []
    for (title, (model, color)) in sorted(my_models.items()):   
        corpora.append(get_spacy(corpus_r, title, model, color))
        
    ## Partie 3. évaluation sans subcorpus
    for corpus in corpora :
        spacy_sans(corpus, corpus_r)

    ## Partie 4. évaluation avec subcorpus
    # ex. avec un corpus : spacy_avec(corpora[1], corpus_r)
    

if __name__ == "__main__":
    main()