#!/usr/bin/env python
#-*- coding: utf-8 -*-


import argparse
import sys
import spacy
import timeit
from tqdm import tqdm
from conllu import parse
from datastructures import Token, Sentence, Corpus

'''
    exemple de ce que l'on peut ecrire sur le terminal
    python3 script/tp1.py -e spacy -r conllu
    soit spacy, le parsing à évaluer
    et conllu, le parsing de reference
'''

def get_spacy() :
    with open(f'./corpus/textebrut.txt', "r") as f : # texte brut recupere a l'avance du fichier conllu
        data = f.readlines()

    nlp = spacy.load("fr_core_news_sm") # on load le modele
    list_sentences = []

    with tqdm(total=len(data), colour="red", desc="spacy") as bar: # sert pour la barre d'avancement, rajoute +1 à chaque phrase analysée
        for line in data :
            doc = nlp(line)
            list_analyses = [] # on cherche à obtenir une liste avec l'analyse de chaque token
            for token in doc:
                list_analyses.append(Token(form=token.text, lemma=token.lemma_, pos=token.pos_))
            list_sentences.append(Sentence(number_tokens=len(doc), analyses=list_analyses))
            bar.update(1) # update la barre
    
    return Corpus(number_lines=len(list_sentences), sentences=list_sentences) # renvoie une instance de la classe Corpus

def get_spacy_retokenize() :
    with open(f'./corpus/textebrut.txt', "r") as f : 
        data = f.readlines()

    nlp = spacy.load("fr_core_news_sm")
    list_sentences = []

    with tqdm(total=len(data), colour="magenta", desc="spacy_retokenize") as bar:
        for line in data :
            doc = nlp(line)
            # with doc.retokenize() as retokenizer:  ==== exemple de rajout d'informations, possibilité de rajouter des règles...
            #     retokenizer.merge(doc[3:5], attrs={"LEMMA": "new york"})
            list_analyses = [] # on cherche à obtenir une liste avec l'analyse de chaque token
            for token in doc:
                list_analyses.append(Token(form=token.text, lemma=token.lemma_, pos=token.pos_))
            list_sentences.append(Sentence(number_tokens=len(doc), analyses=list_analyses))
            bar.update(1)
    
    return Corpus(number_lines=len(list_sentences), sentences=list_sentences) # renvoie une instance de la classe Corpus
               
def get_conllu() :
    with open(f'./corpus/fr_sequoia-ud-test.conllu', "r") as f :
        data = f.read()
    sentences = parse(data)

    with tqdm(total=len(sentences), colour="blue", desc="conllu") as bar:
        list_sentences = []
        for sentence in sentences :
            list_analyses = []
            for token in sentence :
                list_analyses.append(Token(form=token['form'], lemma=token['lemma'], pos=token['upos']))
            list_sentences.append(Sentence(number_tokens=[token['id'] for token in sentence][-1], analyses=list_analyses))
            bar.update(1)

    return Corpus(number_lines=len(list_sentences), sentences=list_sentences) # renvoie une instance de la classe Corpus

parser = argparse.ArgumentParser()
parser.add_argument("-e", help="parsing a evaluer", default="spacy")
parser.add_argument("-r", help="parsing de reference", default="conllu")
args = parser.parse_args()

if args.e == "spacy" :
    corpus_spacy = get_spacy()
    #print(timeit.timeit(stmt="get_spacy()", setup="from __main__ import get_spacy", number=1))

if args.e == "spacy_retokenize" :
    corpus_spacy_retokenize = get_spacy_retokenize()

if args.r == "conllu" :
    corpus_conllu = get_conllu()