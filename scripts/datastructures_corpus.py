#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: agathew
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
# from pathlib import Path

@dataclass
class Token:
    id: int
    forme: str
    lemme: str
    upos: str
    xpos: str
    feats: str
    head: int 
    deprel: str
    deps: str
    misc: str
    is_oov: bool


@dataclass
class Phrase:
    sent_id: str
    text: str
    analyse: List[Token]
    


@dataclass
class Corpus:
    liste_sent: List[Phrase]
    