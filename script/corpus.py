#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: florianj

Description : script de création de l'objet Corpus (contenant l'objet Sentence contenant lui-même l'objet Token) à partir de corpus au format .conllu 

Exemple d'exécution : 
python3 script/corpus-sentences-tokens_extraction.py DATA/fr_sequoia-ud-dev.conllu

"""

from datastructure import Corpus, Sentence, Token
import sys

def make_corpus(file_name:str):
    """
    fonction pour contruire l'objet Corpus à partir du fichier file_name
    """
    type_corpus = file_name.split('-')[2].split('.')[0]

    # initialisation d'une instance de Corpus
    corpus = Corpus(type=type_corpus, sentences=[])

    with open(file_name, 'r') as f:
        next(f) # pour ignorer la première ligne du fichier
        content = f.read()

    sents_info = content[1:].split("\n\n") # contient les metadata + l'analyse de chaque phrase
    # print(sents_info)
    for i in range(len(sents_info) - 1):
        sent_data = sents_info[i].split('\n')
        metadata = [data.split("=")[1].strip() for data in sent_data[:2]]
        
        # initialisation d'une instance de Sentence
        sentence = Sentence(id=metadata[0], text=metadata[1], tokens=[])

        for token in sent_data[2:]:
            token_data = token.split('\t')
            
            if len(token_data) == 10:
                # initialisation d'une instance de Token
                token = Token(*token_data) # syntaxe pour faire correspondre chaque attribut de Token à chaque élément de la liste token_data
                sentence.tokens.append(token)
        
        corpus.sentences.append(sentence)
    return corpus

if __name__ == "__main__":
    file_name = sys.argv[1]

    corpus = make_corpus(file_name=file_name)
    # print(corpus.sentences[0].tokens[0])


