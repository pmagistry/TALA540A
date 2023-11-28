#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    python ./models/train_jiayan
    
Ce fichier sert à ré-entrainer l'outils de posttaging du module jiayan
"""

from jiayan import CRFPOSTagger

postagger = CRFPOSTagger()
print('Building data...')

# pas possible d'utiliser postagger.split_data() à cause de random.shuffle
# all_pos.txt (train + dev) et test.txt => pour entrainement caractère par caractère
# pall_pos.txt (train + dev) et ptest.txt => pour entrainement phrase par phrase
train_x, train_y = postagger.build_data("./corpus/allpos_corpus/pall_pos.txt")
test_x, test_y = postagger.build_data("./corpus/allpos_corpus/ptest.txt")

print('Training...')
postagger.train(train_x, train_y, "models/jiayan/mon_modele_2")
postagger.eval(test_x, test_y, "models/jiayan/mon_modele_2")

