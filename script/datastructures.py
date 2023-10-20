#!/usr/bin/env python
# coding: utf-8

from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    form: str
    pos: str
    is_oov: bool

@dataclass
class Sentence:
    nb_tokens: int # pour vérifier découpage des tokens
    tokens: List[Token]

@dataclass
class Corpus:
    nb_sentences: int
    sentences: List[Sentence]