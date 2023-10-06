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
    feats: Optional[str]
    head: Optional[int] = None
    deprel: Optional[str] = None
    deps: Optional[str] = None
    misc: Optional[str] = None


@dataclass
class Phrase:
    sent_id: str
    text: str
    translit: str
    analyse: List[Token]
    


@dataclass
class Corpus:
    liste_sent: List[Phrase]
    