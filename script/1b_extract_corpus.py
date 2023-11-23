#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    python ./script/2_evaluate.py

Ce fichier compare la tokenisation des modèles spacy et de notre modèle que l'on a entrainé avec une tokenisation de référence
"""

from get_corpus import get_conllu
from datastructures import Token, Sentence, Corpus


def sentence_to_conll(sentence: Sentence) -> str:
    """
    Args:
        sentence (Sentence): contient les informations de chaque token de la phrase

    Returns:
        str: renvoie l'objet Sentence au format conllu
    """
    
    resultat = f"# sent_id = {sentence.sent_id}\n"
    texte = " ".join([token.form for token in sentence.tokens])
    resultat += f"# text = {texte}\n"
    for i, token in enumerate(sentence.tokens):
        resultat += "\t".join([str(i+1), token.form, token.form, token.pos, token.pos, "_", "_", "_", "_", "_"]) + "\n"
    return resultat


def main():
    # on parse le fichier conllu et on crée une instance de la lasse corpus
    corpus = get_conllu("dev")
    # on ne prend les phrases que si elle font partie du sous-corpus que l'on a choisi
    sentences = [ sentence for sentence in corpus.sentences if "KR1h0004" in sentence.sent_id ]
    # on print la phrase au format conllu
    for sentence in sentences:
        print(sentence_to_conll(sentence))


if __name__ == "__main__":
    main()
