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
    
    # ## tables
    # # on parse le fichier conllu
    # with open("lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as f :
    #         data = f.read()
    # tables = parse(data)
    
    # sentences = []
    # # on utilise la tokenisation du fichier conllu
    # for table in tables :
    #     sentences.append([token["form"] for token in table])
    
    ## sentences
    with open("jiayan_corpus/sentence/train.txt", "r", encoding="utf-8") as f :
        data = f.readlines()
       
    sentences = []
    for line in data :
        tokens = line.split("\t")[0]
        sentences.append(tokens.split(" "))        

    model = Word2Vec(sentences=sentences, vector_size=100, window=10, min_count=1, workers=4)
    word_vectors = model.wv
    word_vectors.save_word2vec_format("./vectors/word2vec10.vec")

if __name__ == "__main__":
    main()
    
    
# # table
# 1 Word2Vec(sentences=sentences, vector_size=100, window=3, min_count=1, workers=4)
# 2 Word2Vec(sentences=sentences, vector_size=50, window=3, min_count=1, workers=4)
# 3 Word2Vec(sentences=sentences, vector_size=200, window=3, min_count=1, workers=4)
# 4 Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
# 5 Word2Vec(sentences=sentences, vector_size=100, window=10, min_count=1, workers=4)

# # sentence
# 6 Word2Vec(sentences=sentences, vector_size=100, window=3, min_count=1, workers=4)
# 7 Word2Vec(sentences=sentences, vector_size=50, window=3, min_count=1, workers=4)
# 8 Word2Vec(sentences=sentences, vector_size=200, window=3, min_count=1, workers=4)
# 9 Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
# 10 Word2Vec(sentences=sentences, vector_size=100, window=10, min_count=1, workers=4)