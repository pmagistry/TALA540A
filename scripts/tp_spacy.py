#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spacy
from spacy.tokens import Doc
import re
from dataclasses import dataclass
from typing import List

@dataclass()
class Token:
    forme: str
    lemme: str
    pos: str

@dataclass()
class Corpus:
    phrases : List[str]
    tokens : List[Token]


nlp = spacy.load('fr_core_news_sm')
"""test = nlp("Aux est un test")
for i in test:
    print(i.lemma_, i.pos_)"""
with open("fichierTest.txt",'r') as fichier:
   liste_phrases = fichier.readlines()

reg = re.compile('^\d')
liste_tokens_ref = []
with open("fr_sequoia-ud-test.conllu","r") as reference :
    lines = reference.readlines()
for line in lines:
    #print(line)
    if re.match(reg,line):
        lst = line.split("\t")
        tok = Token(lst[1],lst[2],lst[3])
        liste_tokens_ref.append(tok)
#print(liste_tokens_ref)


corpus = Corpus(liste_phrases,liste_tokens_ref)
#print(corpus)
wordList=[]
lemmaList=[]
posList=[]
for t in corpus.tokens :
    if t.pos != "_":
        wordList.append(t.forme)
        lemmaList.append(t.lemme)
        posList.append(t.pos)
#print(wordList)
#print(lemmaList)
#print(posList)

doc = Doc(nlp.vocab,words=wordList,lemmas=lemmaList,pos=posList)
print(doc.text)

for phrase in liste_phrases:
    dc = nlp(phrase)
    for token in dc:
        print(token.text,token.lemma_,token.pos_)