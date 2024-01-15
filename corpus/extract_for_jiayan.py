#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    python corpus/extract_for_jiayan.py

Ce fichier va extraire les tokens et les pos pour entrainer le module jiayan
qui a besoin d'un corpus dans un format différent que le corpus conllu.
"""

from conllu import parse
import regex


def sentence():
    
    # with open("lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as f :
    #     train = parse(f.read())
        
    with open("lzh_kyoto-ud-test.conllu", "r", encoding="utf-8") as f :
        test = parse(f.read())
    
    with open("lzh_kyoto-ud-dev.conllu", "r", encoding="utf-8") as f :
        dev = parse(f.read())
    
    sentence = {}

    for table in dev:
        
        # 'sent_id' contient le nom du sous-corpus d'où vient la phrase
        sent_id = regex.search(r"^[a-zA-Z0-9]+_[0-9]+_[a-zA-Z0-9]+", table.metadata["sent_id"]).group(0)

        tokens = []
        pos = []
        
        for token in table:
            tokens.append(token["form"])
            pos.append(token["upos"])
        
        if sent_id in sentence.keys():
            for token in tokens :
                sentence[sent_id]['tok'].append(token)
            for tag in pos:
                sentence[sent_id]['pos'].append(tag)
        else :
            sentence[sent_id] = {'tok': tokens,
                                 'pos': pos}
    
    for sent_id in sentence.keys():
        resultat = " ".join(sentence[sent_id]['tok']) + "\t" + " ".join(sentence[sent_id]['pos'])
        print(resultat)
        
def table():

    with open("lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as f :
        train = parse(f.read())
        
    with open("lzh_kyoto-ud-test.conllu", "r", encoding="utf-8") as f :
        test = parse(f.read())

    with open("lzh_kyoto-ud-dev.conllu", "r", encoding="utf-8") as f :
        dev = parse(f.read())

    for table in dev:

        tokens = []
        pos = []
        
        for token in table:
            tokens.append(token["form"])
            pos.append(token["upos"])
        
        resultat = " ".join(tokens) + "\t" + " ".join(pos)
        print(resultat)
        
def word():
    
    with open("lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as f :
        train = parse(f.read())
        
    with open("lzh_kyoto-ud-test.conllu", "r", encoding="utf-8") as f :
        test = parse(f.read())

    with open("lzh_kyoto-ud-dev.conllu", "r", encoding="utf-8") as f :
        dev = parse(f.read())

    for table in dev:
        
        for token in table:
            print(token["form"] + "\t" + token["upos"])

if __name__ == "__main__":
    sentence()
