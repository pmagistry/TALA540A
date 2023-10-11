import sys, argparse, re, conllu, spacy 
from typing import List, Optional, Tuple
from collections import defaultdict
from datastructures import *
from spacy.tokens import Doc

###### Argparse
def arguments() -> argparse: 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", help="fichier texte ou conll" 
    )
    return parser.parse_args()

##### Création de notre structure

#Gestion des espaces pour Doc
def get_misc_space(token : None or dict)-> bool : 
    return True if type(token)=='dict' else False 

# Création des tokens   
def get_token(sentence : str) -> Token :
 
    for token in sentence : 
        yield Token(token["id"],token["form"], token["lemma"], 
                    token["upos"],token["head"], token["deps"],
                    get_misc_space(token["misc"]))
 
# Création des phrases
def get_sentence(data : str) -> Sent : 

    sentences = conllu.parse(data)
    for sentence in sentences : 
        yield Sent(sentence.metadata["text"],
                    [token for token in get_token(sentence)])

#def correct_error(posconll : str, posother : str) -> bool :
    #correct, error = 0, 0
    #return correct + 1, error if posconll == posother else correct, error + 1             


if __name__ == '__main__' : 


#### lecture de notre corpus conll
    args = arguments()

    if args.file.endswith(".conllu") :
        f=open(args.file)
        data=f.read()
        text = [text.metadata["text"] for text in conllu.parse(data)]
        text="".join(text)
        #Création de notre corpus
        corpus = Corpus(text, [sentence for sentence in get_sentence(data)])
        f.close()
        del data # On supprime la variable pour optimiser l'espace mémoire


    # Télchargement du modèle de langue spacy 
    nlp = spacy.load('fr_core_news_sm')

    # Gestion des espaces en français
    # nlp = spacy.blank('fr_core_news_sm')
    
    ######## On va lancer la comparaison entre spacy et conll en liste
    ######## de pos par phrase, on zip et on compare. 

    correct=0
    error=0
    for sent in corpus.sents : 
        
        doc = nlp(sent.text)
        posspacy = [token.pos_ for token in doc] 
        posconll = [token.pos for token in sent.tokens]

        if len(posspacy) == len(posconll) : 
            for spacypos, conllpos in zip(posspacy,posconll) : 
                if spacypos == conllpos : 
                    correct += 1
                else : 
                    error += 1
        elif len(posspacy) > len(posconll) : 
            error += len(posspacy) - len(posconll)
            for spacypos,conllpos in zip(posspacy[0:len(posconll)-1],posconll) :
                if spacypos == conllpos : 
                    correct += 1
                else : 
                    error += 1
        elif len(posspacy) < len(posconll) : 
            error += len(posconll) - len(posspacy)
            for spacypos,conllpos in zip(posspacy,posconll[0:len(posspacy)-1]) :
                if spacypos == conllpos : 
                    correct += 1
                else : 
                    error += 1
    
    print("accuracy : ", correct/(correct+error))

    
