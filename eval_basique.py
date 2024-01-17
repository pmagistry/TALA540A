#!/bin/python3

from typing import List, Union, Dict, Set, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy


@dataclass
class Token:
    form: str
    tag: str
    is_oov: bool
    deprel: str
    parent: int


@dataclass
class Sentence:
    tokens: List[Token]


@dataclass
class Corpus:
    sentences: List[Sentence]


def read_conll(path: Path, vocabulaire: Optional[Set[str]] = None) -> Corpus:
    sentences: List[Sentence] = []
    tokens: List[Token] = []
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
                    deprel = fields[7]
                    parent = int(fields[6])
                    if not "-" in fields[0]:  # éviter les contractions type "du"
                        if vocabulaire is None:
                            is_oov = True
                        else:
                            is_oov = not form in vocabulaire
                        tokens.append(Token(form, tag, is_oov, deprel, parent))
    return Corpus(sentences)


def build_vocabulaire(corpus: Corpus) -> Set[str]:
    return {tok.form for sent in corpus.sentences for tok in sent.tokens}


def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)


def doc_to_sentence(doc: SpacyDoc, origin: Sentence) -> Sentence:
    tokens = []
    for tok, origin_token in zip(doc, origin.tokens):
        #tokens.append(Token(tok.text, tok.pos_, origin_token.is_oov, origin_token.deprel, origin_token.parent))
        tokens.append(Token(tok.text, tok.pos_, origin_token.is_oov, tok.dep_, tok.head.i + 1))
        # tok.head.text => récupère la forme du gouverneur
        # il faut faire -1 car la sortie du parseur est +1 par rapport au fichier conllu.
    return Sentence(tokens)


def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences)


# TODO modifier cette fonction pour compter les UAS, LAS, etc.
"""
LAS: Labeled attachment score (pourcentage de mots attachés à la bonne tête et avec le bon label)
UAS: Unlabeled attachment score (pourcentage de mots attachés à la bonne tête)
OLS: Orthogonal Label Unattached Score (pourcentage de mots attachés au gouverneur avec le bon label, peu importe le gouverneur)
"""
def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus) -> Tuple[float, float]:
    nb_total = 0
    ols = 0
    uas = 0
    las = 0
    oov_total = 0
    oov_ols = 0
    oov_uas = 0
    oov_las = 0

    # matrice de confusion pour le gouverneur
    mc_parent = defaultdict(lambda: defaultdict(int))
    # matrice de confusion pour la relation
    mc_deprel = defaultdict(lambda: defaultdict(int))
    for sentence_gold, sentence_test in zip(
        corpus_gold.sentences, corpus_test.sentences
    ):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert token_gold.form == token_test.form
            nb_total += 1
            uas_ok = False
            ols_ok = False
            mc_parent[token_gold.parent][token_test.parent] += 1 
            mc_deprel[token_gold.deprel][token_test.deprel] += 1
            if int(token_gold.parent) == token_test.parent:
                uas_ok = True
            if token_gold.deprel == token_test.deprel:
                ols_ok = True
            las_ok = uas_ok and ols_ok
            ols += ols_ok
            uas += uas_ok
            las += las_ok
            # TODO gestion des oov
            if token_gold.is_oov:
                oov_total += 1
                oov_ols += ols_ok
                oov_uas += uas_ok
                oov_las += las_ok
    # tag
    if oov_total == 0:
        oov_total += 1
    return ols / nb_total, uas / nb_total, las / nb_total, oov_ols / oov_total, oov_uas / oov_total, oov_las / oov_total, mc_parent, mc_deprel
"""
def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus) -> Tuple[float, float]:
    nb_ok = 0
    nb_total = 0
    oov_ok = 0
    oov_total = 0
    for sentence_gold, sentence_test in zip(
        corpus_gold.sentences, corpus_test.sentences
    ):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert token_gold.form == token_test.form
            if token_gold.tag == token_test.tag:
                nb_ok += 1
            nb_total += 1
            if token_gold.is_oov:
                oov_total += 1
                if token_gold.tag == token_test.tag:
                    oov_ok += 1
    return nb_ok / nb_total, oov_ok / oov_total
"""

def main():
    #model_spacy = spacy.load("fr_core_news_sm")
    #corpus_gold = read_conll("fr_sequoia-ud-test.conllu")

    # tagger du chinois :
    # premier tagger (rapide)
    #model_spacy = spacy.load("../conll_chinois/spacy_model/model-last/")
    # deuxième tagger (performant)
    #model_spacy = spacy.load("../conll_chinois/modele_perf/model_perf_tagger/output/model-best/")
    # troisième parser (performant + transformer)
    #model_spacy = spacy.load("../conll_chinois/modele_perf/model_perf_transformer/output/model-last/")

    # réduction des données d'entraînement
    #model_spacy = spacy.load("../conll_chinois/modele_perf/modele_perf_100k/output/model-last/")
    model_spacy = spacy.load("../conll_chinois/modele_perf/modele_perf_250k/output/model-last/")

    # Etat de l'art: modèle de spacy
    #model_spacy = spacy.load("zh_core_web_trf")
    corpus_gold = read_conll("../conll_chinois/test.conllu", vocabulaire = set(model_spacy.vocab.strings))

    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    ols, uas, las, ools, ouas, olas, mc_parent, mc_deprel = compute_accuracy(corpus_gold, corpus_test)
    print("Score OLS:", ols)
    print("Score UAS:", uas)
    print("Score LAS:", las)
    print("\nOOV")
    print("Score OLS:", ools)
    print("Score UAS:", ouas)
    print("Score LAS:", olas)


if __name__ == "__main__":
    main()
