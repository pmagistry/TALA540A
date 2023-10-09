from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Token : 
    id :int
    text : str
    lemma : str
    pos : str
    head : int
    dep : str
    misc : str

@dataclass 
class Sent :
    text : str
    tokens : List[Token]

@dataclass 
class Corpus : 
    text : str 
    sents : List[Sent]
