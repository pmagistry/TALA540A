import argparse, spacy 
from pathlib import Path
from typing import List

from datastructures import *
from spacy import Language as SpacyPipeline
from spacy.tokens import Doc as SpacyDoc

###### Argparse
def arguments() -> argparse: 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", help="fichier texte ou conll" 
    )
    return parser.parse_args()

##### Read Conll 
def read_conll(path : Path) -> Corpus : 

    sentences = []    
    tokens = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                if line == "":
                    sentences.append(Sent(tokens))
                    tokens = []
                else:
                    fields = line.split("\t")
                    form, pos = fields[1], fields[3]
                    if not "-" in fields[0]: # éviter les contractions type "du"
                        tokens.append(Token(form, pos))
    return Corpus(sentences)            

####### Création des corpus de test 

def sentence_to_doc(sentence: Sent, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)

def doc_to_sentence(doc: SpacyDoc) -> Sent:
    tokens = []
    for tok in doc:
        tokens.append(Token(tok.text, tok.pos_))
    return Sent(tokens)

def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline ) -> Corpus:
    sentences = []
    for sentence in corpus.sents:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc))
    return Corpus(sentences)


####### Calcul de la précision 
def compute_accuracy(gold_list : Corpus, test_list : Corpus) -> float:
    correct = 0 
    total = 0 
    for gold_sentence, test_sentence in zip(gold_list.sents, test_list.sents) : 
        for gold_token, test_token in zip(gold_sentence.tokens, test_sentence.tokens) : 
            assert (gold_token.form == test_token.form)
            total += 1
            if gold_token.pos == test_token.pos : 
                correct +=1
        
    return correct/total

if __name__ == '__main__' : 


#### lecture de notre corpus conll
    args = arguments()

    if args.file.endswith(".conllu") :
        corpus_gold = read_conll(args.file)
    
    model_spacy = spacy.load("fr_core_news_sm")
    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    print(compute_accuracy(corpus_gold, corpus_test))