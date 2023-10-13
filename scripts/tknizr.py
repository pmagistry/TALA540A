import argparse, spacy 
from pathlib import Path
from typing import List, Set, Dict, Tuple

from datastructures import *
from spacy import Language as SpacyPipeline
from spacy.tokens import Doc as SpacyDoc

###### Argparse
def arguments() -> argparse: 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "gold", help="fichier texte ou conll"      
    )
    parser.add_argument(
        "ref", help="fichier texte ou conll", nargs = "?"      
    )
    return parser.parse_args()

##### Read Conll 
def read_conll(path : Path, vocab: Optional[Set[str]] = None) -> Tuple[Corpus, Set[str]] : 

    sentences = []    
    tokens = []
    vocabulary = set()
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
                    vocabulary.add(form)
                    if not "-" in fields[0]: # éviter les contractions type "du"
                        if vocab is None : 
                            is_oov = True
                        else : 
                            is_oov = not form in vocab
                        tokens.append(Token(form, pos, is_oov))
    return Corpus(sentences), vocabulary             

####### Création des corpus de test 

def sentence_to_doc(sentence: Sent, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)

def doc_to_sentence(doc: SpacyDoc, origin : Sent) -> Sent:
    tokens = []
    for tok, origin_tok in zip(doc, origin.tokens):
        tokens.append(Token(tok.text, tok.pos_, is_oov = origin_tok.is_oov))
    return Sent(tokens)

def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline ) -> Corpus:
    sentences = []
    for sentence in corpus.sents:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences)

####### Calcul de la précision 
def compute_accuracy(gold_list : Corpus, test_list : Corpus) -> float:
    correct = 0 
    total = 0 
    oov_total = 0
    oov_ok =0
    for gold_sentence, test_sentence in zip(gold_list.sents, test_list.sents) : 
        for gold_token, test_token in zip(gold_sentence.tokens, test_sentence.tokens) : 
            assert (gold_token.form == test_token.form)
            total += 1
            if gold_token.pos == test_token.pos : 
                correct +=1
            if gold_token.is_oov:
                oov_total += 1
                if gold_token.pos == test_token.pos:
                    oov_ok += 1

    return correct / total, oov_ok / oov_total

if __name__ == '__main__' : 

#### lecture de notre corpus conll
    args = arguments()

    if args.ref : 
        if args.ref.endswith(".conllu") : 
            corpus_ref, vocab_ref = read_conll(args.ref)
            
    print(len(vocab_ref))
    if args.gold.endswith(".conllu") :

        corpus_gold, vocab_gold = read_conll(args.gold, vocab_ref)


    model_spacy = spacy.load("fr_core_news_sm")
    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    print(compute_accuracy(corpus_gold, corpus_test))