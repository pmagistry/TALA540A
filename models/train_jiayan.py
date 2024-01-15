#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    python ./models/train_jiayan
    
Ce fichier sert à ré-entrainer l'outils de posttaging du module jiayan
"""

from crf_pos_tagger import CRFPOSTagger

tagger = CRFPOSTagger()

print('Building data...')

train_x, train_y = tagger.build_data("./corpus/jiayan_corpus/word/corpus.txt")
test_x, test_y = tagger.build_data("./corpus/jiayan_corpus/word/test.txt")

print('Training...')
tagger.train(train_x, train_y, "models/jiayan/modele_word")
tagger.eval(test_x, test_y, "models/jiayan/modele_word")

