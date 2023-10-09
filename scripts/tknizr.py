import sys, argparse, re, conllu, spacy 
from typing import List, Optional
from datastructures import *
from spacy.tokens import Doc


def arguments() -> argparse: 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", help="fichier texte ou conll" 
    )
    return parser.parse_args()

def get_token(sentence : str) -> Token :
 
    for token in sentence : 
        yield Token(token["id"],token["form"], token["lemma"], 
                    token["upos"],token["head"], token["deps"], token["misc"])
 
def get_sentence(data : str) -> Sent : 

    sentences = conllu.parse(data)
    for sentence in sentences : 
        yield Sent(sentence.metadata["text"],
                    [token for token in get_token(sentence)])


if __name__ == '__main__' : 

    args = arguments()

    if args.file.endswith(".conllu") :
        f=open(args.file)
        data=f.read()
        text = [text.metadata["text"] for text in conllu.parse(data)]
        text="".join(text)
        corpus = Corpus(text, [sentence for sentence in get_sentence(data)])
        f.close()
        del data

#print(corpus.sents[1])

spacy.load('fr_core_news_sm')

nlp = spacy.blank('fr')


for sentence in corpus.sents : 
    words = [token.text for token in sentence.tokens]
    spaces = []
    pos = []
    for token in sentence.tokens : 
        if token.misc == None :
            spaces.append(True)
        else :
            spaces.append(False)
    for token in sentence.tokens : 
        if token.pos == "_" : 
            pos.append("ADP")
        else : 
            pos.append(token.pos)
    lemmas = [token.lemma for token in sentence.tokens]
    heads = [token.head for token in sentence.tokens]
    deps = [token.dep for token in sentence.tokens]
    #spaces = [if token.misc == None : False else : True for token in sentence.tokens]
    doc = Doc(nlp.vocab,
              words=words,
              spaces=spaces,
              pos=pos,
              lemmas=lemmas,
              heads=heads,
              deps=deps) 

    print (doc.text)