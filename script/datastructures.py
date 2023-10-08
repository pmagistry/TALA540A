#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    form: str
    lemma: str
    pos: str

@dataclass
class Sentence:
    number_tokens: int  # pour savoir si le découpage par tokens est le même
    analyses: List[Token]

@dataclass
class Corpus:
    number_lines: int # pour savoir si le découpage par ligne s'est bien passé
    sentences: List[Sentence]