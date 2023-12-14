#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier corpus :
    python extract_vectors.py

Ce fichier va vectoriser le corpus pour ensuite l'utiliser pour l'entrainement
"""

from conllu import parse
from gensim.models import Word2Vec



def main():
    
    # on parse le fichier conllu
    with open("lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as f :
            data = f.read()
    tables = parse(data)
    
    sentences = []
    # on utilise la tokenisation du fichier conllu
    for table in tables :
        sentences.append([token["form"] for token in table])

    model = Word2Vec(sentences=sentences, vector_size=100, window=3, min_count=1, workers=4)
    word_vectors = model.wv
    word_vectors.save_word2vec_format("word2vec.vec")

if __name__ == "__main__":
    main()