from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Token:
	forme:str
	lemme:str
	pos:str
	
@dataclass
class Sentence:
	taille:int
	token:Token