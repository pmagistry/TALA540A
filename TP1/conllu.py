# lecture fichier conll-u avec stanza 

import spacy
import stanza
import spacy_stanza
from spacy_conll import init_parser
from dataclasses import dataclass
from pprint import pprint 
from spacy.training import Alignment
from collections import defaultdict  

conll_list = []
spacy_list = []

# dataclass
@dataclass
class Token:
    forme: str
    pos: str  


# pos sequoi
nlp = init_parser("fr",
                  "stanza")

nlp_spacy = spacy.load("fr_core_news_sm")

# read file 
f = open('fr_sequoia.txt', 'r')
conll_text = f.read()
doc1 = nlp(conll_text)
for token in doc1:
    #print(token.text, token.pos_)
    conll_list.append(Token(token.text, token.pos_))

#pprint(f'connl_List = {conll_list}')

# pos spacy 
doc2 = nlp_spacy(conll_text)
for token in doc2:
    spacy_list.append((Token(token.text, token.pos_)))


#pprint(f'spacy_list = {spacy_list}')

# Calcul accuracy 
dict_conll = defaultdict(lambda : defaultdict(int))
spacy_dict = defaultdict(lambda: defaultdict(int))

for item in conll_list:
    dict_conll[item.forme][item.pos] += 1

#pprint(dict_conll)
#print(len(dict_conll))

for all in spacy_list:
    spacy_dict[all.forme][all.pos] += 1


#### def 
def get_difference(dict1, dict2, currentCount):
    if dict1.keys() != dict2.keys():
        total = sum(dict1.values())
        currentCount  += total
        # print(dict1.keys(), dict1.values())
        # print(dict2.keys(), dict2.values())

    return currentCount


# par token
currentCount = 0
allCount = []

for token in dict_conll.keys():
    if token in spacy_dict.keys():
        if dict_conll[token] != spacy_dict[token]:
            currentCount = get_difference(dict_conll[token] , spacy_dict[token], currentCount)
            #print(dict_conll[token] , spacy_dict[token])

            

#print(f'current count = {currentCount}')

allCount = len(spacy_list)
#print(f'all count = {allCount}')

print(f'accuracy des POS fichiers conllu = {(1-(currentCount/allCount))*100}')
