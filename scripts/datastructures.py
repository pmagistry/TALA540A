from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Token : 
    form : str
    pos : str
    is_oov: bool

@dataclass 
class Sent :
    sent_id : str
    tokens : List[Token]

@dataclass 
class Corpus : 
    sents : List[Sent]