'''
Étape 1 
'''

import spacy 

chemin_fichier = "resultats.txt"

with open(chemin_fichier, "r", encoding="utf-8") as file:
    texte = file.read()

nlp = spacy.load ("fr_core_news_sm")

def tokenize_text(texte):
    doc = nlp(texte)
    tokens = [token.text for token in doc]
    return tokens

print(tokenize_text(texte))

'''
# 2. tokenisation de sequoia 
doc = nlp("resultats.txt")
from spacy.tokens import Doc 


words = ["hello", "world", "!"]
spaces = [True, False, False]
doc = Doc(nlp.vocab, words=words, spaces=spaces)

print(doc)
'''
