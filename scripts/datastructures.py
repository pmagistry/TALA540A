#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : tifanny
"""

from typing import List
from dataclasses import dataclass

@dataclass
class Token:
    #id : int
    forme : int
    #lemme : int
    #upos : int
    tag : int

@dataclass
class Phrase:
    #phr_id : int
    #texte : int
    token : List[Token]

@dataclass
class Corpus:
    contenu : List[Phrase]

def read_conll(path: Path) -> Corpus:
    pass

def tag_corpus(corpus: Corpus, model_spacy:...) -> Corpus:
    pass
    
def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus) -> float:
    pass