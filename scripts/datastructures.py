#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : tifanny
"""

from typing import List
from dataclasses import dataclass

@dataclass
class Token:
    id : int
    forme : int
    lemme : int
    upos : int

@dataclass
class Phrase:
    phr_id : int
    texte : int
    token : List[Token]

@dataclass
class Corpus:
    contenu : List[Phrase]