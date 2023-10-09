#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
from get_function import get_spacy, get_spacy_retokenize, get_conllu, get_pos, get_accuracy, get_precision, get_rappel

'''
    exemple de ce que l'on peut ecrire sur le terminal
    python3 script/tp1.py -e spacy_retokenize
    soit spacy_retokenize, le parsing à évaluer
'''

parser = argparse.ArgumentParser()
parser.add_argument("-e", help="parsing a evaluer", default="spacy")
args = parser.parse_args()


if args.e == "spacy_retokenize" :
    sentences_conllu, corpus_conllu = get_conllu()
    # print(timeit.timeit(stmt="get_conllu()", setup="from __main__ import get_conllu", number=1))
    lpos_r, pos_r = get_pos(corpus_conllu)

    corpus_spacy_retokenize = get_spacy_retokenize(sentences_conllu)
    # print(timeit.timeit(stmt="get_spacy_retokenize(sentences_conllu)", setup="from __main__ import get_spacy_retokenize(sentences_conllu)", number=1))
    lpos_e, pos_e = get_pos(corpus_spacy_retokenize)

else : # par defaut, parsing spacy
    sentences_conllu, corpus_conllu = get_conllu()
    # print(timeit.timeit(stmt="get_conllu()", setup="from __main__ import get_conllu", number=1))
    lpos_r, pos_r = get_pos(corpus_conllu)

    corpus_spacy = get_spacy()
    # print(timeit.timeit(stmt="get_spacy()", setup="from __main__ import get_spacy", number=1))
    lpos_e, pos_e = get_pos(corpus_spacy)


print(f"\nnombre de pos dans le corpus de reference : {len(pos_r)}\nnombre de pos dans le corpus a evaluer : {len(pos_e)}")
print(f"l'accuracy est à {round(get_accuracy(lpos_r, lpos_e, pos_e) * 100, 2)}%")
print(f"la precision pour la classe \'DET\' est à {round(get_precision(lpos_r, lpos_e, pos_e, 'DET') * 100, 2)}%")
print(f"le rappel pour la classe \'DET\' est à {round(get_rappel(lpos_r, lpos_e, pos_r, 'DET') * 100, 2)}%")