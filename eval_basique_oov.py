#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du 12.10
18.10 : ajout pr distinguer les OOV
"""

from typing import List, Union, Dict
from pathlib import Path
from dataclasses import dataclass

import spacy
from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc

from sklearn.metrics import confusion_matrix

import timeit


@dataclass
class Token():
    #id : int
    form : str
    #lemme : int
    #upos : int
    tag : str
    is_oov : bool

@dataclass
class Sentence():
    #phr_id : int
    #texte : int
    tokens : List[Token]

@dataclass
class Corpus():
    sentences : List[Sentence]

def read_conll(path: Path, vocab) -> Corpus:
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
                        if vocab is None:
                            is_oov = True
                        else:
                            is_oov = not form in vocab
                        tokens.append(Token(form, tag, is_oov))

    return Corpus(sentences)

def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)

def doc_to_sentence(doc: SpacyDoc) -> Sentence:
    tokens = []
    for token in doc:
        tokens.append(Token(token.text, token.pos_, is_oov=token.is_oov))
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

def compute_accuracy_with_oov(corpus_gold: Corpus, corpus_test: Corpus, vocab: set) -> float:
    nb_ok = 0
    nb_total = 0
    oov_nb = 0
    oov_total = 0
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert(token_gold.form == token_test.form)
            if token_gold.tag == token_test.tag:
                nb_ok += 1
            nb_total += 1

            # Vérifie si le token est OOV (hors du vocabulaire Sequoia)
            if token_test.is_oov or token_test.form not in vocab:
                oov_total += 1
                if token_gold.tag == token_test.tag:
                    oov_nb += 1

    #accuracy = nb_ok / nb_total
    oov_accuracy = oov_nb / oov_total if oov_total > 0 else 0.0
    return oov_accuracy

def accuracy(corpus_gold, corpus_test, vocab):
    acc = compute_accuracy_with_oov(corpus_gold, corpus_test, vocab)
    acc_pourcentage = acc * 100
    print(f'Accuracy : {acc_pourcentage:.2f}%')

def matrice_confusion(corpus_gold, corpus_test):
    y_true = []  
    y_pred = []  

    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            y_true.append(token_gold.tag)
            y_pred.append(token_test.tag)
    
    # Créer la matrice de confusion
    confusion = confusion_matrix(y_true, y_pred)

    return confusion

def main():
    model_spacy = spacy.load("fr_core_news_sm")

    vocab = sequoia_voc("./corpus/fr_sequoia-ud-train.conllu")
    corpus_gold = read_conll("./corpus/fr_sequoia-ud-test.conllu", vocab=vocab)
    corpus_test = tag_corpus(corpus_gold, model_spacy)

    # Mesurer le temps que prend le programme pr s'éxecuter 

    time = timeit.timeit(lambda: accuracy(corpus_gold, corpus_test, vocab), number = 1)

    # Créer la matrice

    confusion = matrice_confusion(corpus_gold, corpus_test)

    print(f"Temps de l'exécution : {time:.2f} seconds")
    print("Confusion Matrix:")
    print(confusion)

if __name__ == "__main__":
    main()
    