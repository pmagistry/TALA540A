#!/usr/bin/env python
# coding: utf-8

from typing import List, Optional
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    id: int
    forme: str
    lemme: str
    upos: str
    xpos: str
    feats: Optional[str]
    head: Optional[int] = None
    deprel: Optional[str] = None
    deps: Optional[str] = None
    misc: Optional[str] = None

@dataclass
class Sentence:
    text : str
    tokens : List[Token]

@dataclass
class Corpus:
    text : str 
    sents : List[Sentence]