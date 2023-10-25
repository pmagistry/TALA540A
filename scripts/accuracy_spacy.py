#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Set, Tuple
import sys, spacy
from datastructures_corpus import Corpus, Phrase, Token
from spacy.tokens import Doc

# from pprint import pprint


def make_corpus_conll(file: str, vocabulaire: Optional[Set[str]] = None):
    with open(file, "r") as f:
        content = f.read()
        # Initialisation d'une instance de Corpus
        corpus = Corpus([])
        # Création d'une liste où chaque élément est une phrase (métadonnées + analyse)
        sents = content.split("\n\n")
        for i in range(len(sents) - 1):
            # Initialisation phrase
            sentence = Phrase("", "", [])
            # On a une liste d'éléments par phrase (metadata + analyse Token)
            sent_data = sents[i].split("\n")
            meta = []
            for data in sent_data:
                # Les metadata commencent par un #
                if data.startswith("#"):
                    meta.append(data)
                    # Initialisation d'une instance de Phrase
                    for d in meta:
                        if "sent_id" in d:
                            sentence.sent_id = d.split(" = ")[1]
                        if "text" in d:
                            sentence.text = d.split(" = ")[1]
                else:
                    token_ana = data.split("\t")
                    # éviter les contractions type "du"
                    if not "-" in token_ana[0]:
                        if vocabulaire is None:
                            token_ana.append(True)
                        else:
                            token_ana.append(not token_ana[1] in vocabulaire)
                        # Permet de faire correspondre à chaque élément de la liste l'attribut associé en fonction de l'ordre/indice
                        sentence.analyse.append(Token(*token_ana))
            corpus.liste_sent.append(sentence)
    return corpus


def make_corpus_spacy(
    corpus_gold: Corpus, spacy_model, vocabulaire: Optional[Set[str]] = None
) -> Corpus:
    corpus_spacy = Corpus([])
    nlp = spacy.load(spacy_model)
    for sent in corpus_gold.liste_sent:
        sent_spacy = Phrase("", "", [])
        sent_spacy.text = sent.text
        sent_spacy.sent_id = sent.sent_id
        compt = 1
        # permet de prendre en compte les formes décontractées (de le)
        doc = Doc(nlp.vocab, words=[t.forme for t in sent.analyse])
        for tok in nlp(doc):
            # print(tok.pos_)
            if vocabulaire is None:
                tok_spacy = Token(
                    compt,
                    tok.text,
                    tok.lemma_,
                    tok.pos_,
                    tok.tag_,
                    "",
                    "",
                    "",
                    "",
                    "",
                    True,
                )
            else:
                is_oov = not tok.text in vocabulaire
                tok_spacy = Token(
                    compt,
                    tok.text,
                    tok.lemma_,
                    tok.pos_,
                    tok.tag_,
                    "",
                    "",
                    "",
                    "",
                    "",
                    is_oov,
                )
            compt += 1
            sent_spacy.analyse.append(tok_spacy)
        corpus_spacy.liste_sent.append(sent_spacy)
    return corpus_spacy


def compar_listes(
    corpus_gold: Corpus,
    corpus_test: Corpus,
    subcorpus: Optional[str] = None,
    conf_matrix: Optional[bool] = False,
) -> Tuple(float, float):
    compt_true = 0
    compt_tot = 0
    oov_ok = 0
    oov_total = 0
    pos_gold = []
    pos_spacy = []
    for sent_gold, sent_test in zip(corpus_gold.liste_sent, corpus_test.liste_sent):
        if subcorpus is None or subcorpus in sent_gold.sent_id:
            for token_gold, token_test in zip(sent_gold.analyse, sent_test.analyse):
                assert token_gold.forme == token_test.forme
                pos_gold.append(token_gold.upos)
                pos_spacy.append(token_test.upos)
                if token_gold.upos == token_test.upos:
                    compt_true += 1
                compt_tot += 1
                if token_gold.is_oov:
                    oov_total += 1
                    if token_gold.upos == token_test.upos:
                        oov_ok += 1
    if conf_matrix:
        sns.heatmap(
            confusion_matrix(pos_gold, pos_spacy),
            annot=True,
            cmap="Blues",
            xticklabels=list(set(pos_gold)),
            yticklabels=list(set(pos_gold)),
        )
        plt.xlabel("POS spacy")
        plt.ylabel("POS corpus")
        plt.show()
    return compt_true / compt_tot, oov_ok / oov_total


def make_vocab(corpus: Corpus):
    return {tok.forme for sent in corpus.liste_sent for tok in sent.analyse}


def corpus_list(corpus_train: Corpus):
    return [sent.sent_id.rsplit("_", 1) for sent in corpus_train.liste_sent]


if __name__ == "__main__":
    # corpus train utilisé pour faire le vocabulaire
    corpus_train = sys.argv[1]

    corpus_test = sys.argv[2]
    model = sys.argv[3]

    # Création du vocabulaire à partir du corpus train
    c_train = make_corpus_conll(corpus_train)

    vocab = make_vocab(c_train)

    # Création du Corpus à partir du corpus de test
    c_gold = make_corpus_conll(corpus_test, vocab)

    # Création du Corpus spacy à partir du corpus gold
    c_test = make_corpus_spacy(c_gold, model, vocab)

    acc_tok, acc_oov = compar_listes(c_gold, c_test, True)
    print(
        f"L'accuracy moyenne du modèle {model} de spacy sur ce corpus est de : {acc_tok} et l'accuracy sur les mots non-présents dans le vocabulaire est de : {acc_oov}"
    )
