# -*- coding: utf-8 -*-

"""
Classes de données du projet:

- Token
- Document
- Corpus

"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Token:
	form: str
	lemma: str
	pos: str

@dataclass
class Sentence:
	sentence: str
	tokens: List[Token]

@dataclass
class Document:
	sentences: List[Sentence]

@dataclass
class Corpus:
	documents: List[Document]
