#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: florianj
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Token:
    id: int
    form: str
    lemma: str
    upos: str
    xpos: Optional[str] = None
    feats: Optional[list] = None
    head: Optional[str] = None
    deprel: Optional[str] = None
    deps: Optional[str] = None
    misc: Optional[str] = None

@dataclass
class Sentence:
    id: str
    text: str
    tokens: List[Token]
    
@dataclass
class Corpus:
    type: str
    sentences: List[Sentence]
    



