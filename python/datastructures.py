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
    tag: str
    dep: str
    shape: str
    alpha: bool
    stop: bool

@dataclass
class Sentence:
    text: str
    length: int
    analyse: List[Token]

@dataclass
class Corpus:
    categories: List[str]
    begin: str
    end: str
    chemin: Path
    articles: List[Article]