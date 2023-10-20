#!/usr/bin/env python
# coding: utf-8

""" Ce fichier contient les classes utilisées par tous les autres fichiers
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    """Chaque objet de la classe Token contiendra
    
    form -- la forme du mot
    pos -- son pos
    is_oov -- s'il fait partie du vocabulaire du corpus de reference ou non
    """

    form: str
    pos: str
    is_oov: bool


@dataclass
class Sentence:
    """Chaque objet de la classe Sentence contiendra
    
    nb_tokens -- le nombre de tokens dans la phrase
    tokens -- la liste d'objets de la classe Token
    """

    nb_tokens: int
    tokens: List[Token]


@dataclass
class Corpus:
    """Chaque objet de la classe Corpus contiendra
    
    nb_sentences -- le nombre de phrases dans le corpus
    sentences -- la liste d'objets de la classe Sentence
    """

    nb_sentences: int
    sentences: List[Sentence]
