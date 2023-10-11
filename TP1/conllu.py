# lecture fichier conll-u avec stanza 

import spacy
import stanza
import spacy_stanza
from spacy_conll import init_parser
from dataclasses import dataclass
from pprint import pprint 
from spacy.training import Alignment

conll_list = []
spacy_list = []

# dataclass
@dataclass
class Token:
    forme: str
    pos: str  


# pos sequoi
nlp = init_parser("fr",
                  "stanza",
                  parser_opts={"use_gpu": False, "verbose": True},
                  ext_names={"conll_pd": "pandas"},
                  include_headers=True)

nlp_spacy = spacy.load("fr_core_news_sm")

# read file 
f = open('fr_sequoia.txt', 'r')
conll_text = f.read()
doc1 = nlp(conll_text[:200])
for token in doc1:
    #print(token.text, token.pos_)
    conll_list.append(Token(token.text, token.pos_))
pprint(f'connl_List = {conll_list}')

# pos spacy 
doc2 = nlp_spacy(conll_text[:200])
for token in doc2:
    spacy_list.append((Token(token.text, token.pos_)))


pprint(f'spacy_list = {spacy_list}')

# Calcul accuracy 