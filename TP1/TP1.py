'''
Étape 1 : 

Utilisation de l'envrionnement "myenv"
Ligne de commande : conda activate myenv 

Version texte brut : cat fr_sequoia-ud-test.conllu | grep "# text" | sed 's/# text = //'
> fichier : resultats.txt

'''


# 1ère version d'une tokenisation de sequoia 

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
'''
# 2. tokenisation de sequoia 
doc = nlp("resultats.txt")
from spacy.tokens import Doc 


words = ["hello", "world", "!"]
spaces = [True, False, False]
doc = Doc(nlp.vocab, words=words, spaces=spaces)

print(doc)
'''

# Correction 

#importation de modules

from typing import List, Union, Dict 
from pathlib import Path 
from dataclasses import dataclass 

from spacy import Language
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc 
import spacy 

@dataclass
class Token():
    form : str 
    tag : str 

@dataclass
class Sentence():
    tokens: List[Token]


@dataclass
class Corpus():
    sentences: List[Sentence]


def read_conll(path: Path ) -> Corpus : 
    sentences = []
    with open(path) as f: 
        for line in f: 
            line = line.strip()
            if not line.startswith('#'): 

                if line == "": 
                    sentences.append(sentences(tokens))
                    tokens = []
                else : 
                    fields = line.split("\t")
                    form, tag = fields[1], fields[3]
                    if not tag == "_" : 
                        tokens.append(Token(form,tag))
    return Corpus (sentences)

def tag_corpus(corpus: Corpus,model_spacy: spacy.language) -> Corpus : 
    pass 
               
def compute_accuracy(corpus_gold: Corpus, corpus_test:Corpus) -> float: 
    nb_ok = 0
    nb_total = 0   
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens): 
            assert(token_gold.form == token_test.form )
            if token_gold.tag == token_test.tag : 
                nb_ok+= 1 
            nb_total += 1 
    return nb_ok /nb_total


def main():
    corpus_gold = read_conll("fr_sequoia-ud-test.conllu")
    print (corpus_gold)

# if __name__ == 