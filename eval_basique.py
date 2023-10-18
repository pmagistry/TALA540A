#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du 12.10
"""

from typing import List, Union, Dict
from pathlib import Path
from dataclasses import dataclass

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy

@dataclass
class Token():
    #id : int
    form : str
    #lemme : int
    #upos : int
    tag : str

@dataclass
class Sentence():
    #phr_id : int
    #texte : int
    tokens : List[Token]

@dataclass
class Corpus():
    sentences : List[Sentence]

def read_conll(path: Path) -> Corpus:
    sentences = []
    tokens = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#"):

                if line == "":
                    sentences.append(Sentence(tokens))
                    tokens = []
                else:
                    fields = line.split("\t")
                    form, tag = fields[1], fields[3]
                    if not "-" in fields[0]: # Eviter les contractions type "du"
                        tokens.append(Token(form, tag))
    return Corpus(sentences)

def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)

def doc_to_sentence(doc: SpacyDoc) -> Sentence:
    tokens = []
    for tok in doc:
        tokens.append(Token(tok.text, tok.pos_))
    return Sentence(tokens)

def tag_corpus(corpus: Corpus, model_spacy: SpacyPipeline ) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc))
    return Corpus(sentences)

def sequoia_voc(train_path: Path) -> set:
    vocabulary = set()
    with open(train_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#") and line:
                fields = line.split("\t")
                word = fields[1]
                vocabulary.add(word)
    return vocabulary

def compute_accuracy_with_oov(corpus_gold: Corpus, corpus_test: Corpus, sequoia_train_vocab: set) -> float:
    nb_ok = 0
    nb_total = 0
    nb_oov = 0
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert(token_gold.form == token_test.form)
            if token_gold.tag == token_test.tag:
                nb_ok += 1
            nb_total += 1

            # Vérifie si le token est OOV (hors du vocabulaire Sequoia)
            if token_test.form not in sequoia_train_vocab:
                nb_oov += 1

    accuracy = nb_ok / nb_total
    accuracy_percentage = accuracy * 100
    return accuracy, accuracy_percentage, nb_oov
    
'''def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus) -> float:
    nb_ok = 0
    nb_total = 0
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert(token_gold.form == token_test.form)
            if token_gold.tag == token_test.tag:
                nb_ok += 1
            nb_total += 1
        return nb_ok / nb_total '''

def main():
    model_spacy = spacy.load("fr_core_news_sm")
    corpus_gold = read_conll("../corpus/fr_sequoia-ud-test.conllu")
    corpus_test = tag_corpus(corpus_gold, model_spacy)

    accuracy = compute_accuracy(corpus_gold, corpus_test)
    acc_pourcentage = accuracy * 100
    print(f'Accuracy : {acc_pourcentage:.2f}%')


if __name__ == "__main__":
    main()
    