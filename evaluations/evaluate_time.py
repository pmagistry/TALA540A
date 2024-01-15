#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    $ python evaluations/evaluate_spacy.py

    Ce fichier compare la tokenisation des modèles spacy 
    et de notre modèle que l'on a entrainé avec une tokenisation de référence
"""

from get_corpus import get_conllu, get_spacy, get_jiayan

def main():
    
    # les modèles
    # (corpus_r, "corpus_lg", "zh_core_web_lg", "GREEN")
    # (corpus_r, "corpus_md", "zh_core_web_md", "CYAN")
    # (corpus_r, "corpus_sm", "zh_core_web_sm", "MAGENTA")
    # (corpus_r, "corpus_trf", "zh_core_web_trf", "RED")
    # (corpus_r, "corpus_jiayan", "./models/jiayan/modele_jiayan", "BLUE")
    # (corpus_r, "corpus_sentence", "./models/jiayan/modele_sentence", "YELLOW")
    # (corpus_r, "corpus_table", "./models/jiayan/modele_table", "GREEN")
    # (corpus_r, "corpus_word", "./models/jiayan/modele_word", "RED")

    corpus_train = get_conllu("train")
    vocabulaire = {token.form for sentence in corpus_train.sentences for token in sentence.tokens}
    corpus_r = get_conllu("test", vocabulaire)
    get_jiayan(corpus_r, "corpus_word", "./models/jiayan/modele_word", "RED")

if __name__ == "__main__":
    main()