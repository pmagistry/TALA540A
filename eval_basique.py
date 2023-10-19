from typing import List, Union, Dict, Set, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy

import timeit

import pandas as pd
from sklearn.metrics import confusion_matrix


@dataclass
class Token:
    form: str
    tag: str
    is_oov: bool


@dataclass
class Sentence:
    sent_id : str
    tokens: List[Token]


@dataclass
class Corpus:
    sentences: List[Sentence]

"""
objectif à revoir : split le corpus en 4 sous corpus --> remis à plus tard
"""
# Création de l'objet Corpus
def read_conll(path: Path, vocabulaire: Optional[Set[str]] = None) -> Corpus:
    sentences = []
    tokens = []  # objet Token
    with open(path) as f:
        for line in f:
            line = line.strip()  # retire les espaces début et fin
            if not line.startswith("#"):
                # vérifie si la ligne lue à partir du fichier CoNLL est vide
                # une ligne vide est utilisée pour indiquer la fin d'une phrase.
                # Si la condition est vraie la boucle a atteint la fin de la phrase actuelle
                if line == "":
                    sentences.append(Sentence(tokens))
                    tokens = (
                        []
                    )  # form, tag, is_oov --> réinitialiser pour chaque phrase
                else:
                    fields = line.split("\t")
                    form, tag = fields[1], fields[3]
                    if not "-" in fields[0]:  # éviter les contractions type "du"
                        if vocabulaire is None:
                            is_oov = True
                        else:
                            is_oov = not form in vocabulaire
                        tokens.append(Token(form, tag, is_oov))
    # print(Corpus(sentences))
    return Corpus(sentences)


# permet de crée un document qu'on peut analyser avec les options de spacy .text, .pos_ ....
# à la place d'utiliser doc = nlp() où nlp est le modèle de langage
def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)


# converti un objet SpacyDoc en une instance de la classe Sentence
# représente la même phrase dans un format compatible avec spaCy
def doc_to_sentence(doc: SpacyDoc, origin: Sentence) -> Sentence:
    tokens = []
    for tok, origin_token in zip(doc, origin.tokens):
        tokens.append(Token(tok.text, tok.pos_, is_oov=origin_token.is_oov))
    return Sentence(tokens)


# prend un corpus de phrases, l'annote à l'aide d'un modèle spaCy
# puis renvoie un nouveau corpus contenant les phrases annotées.
def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences)


# extraction du vocabulaire du corpus train
def vocab_train(path: Path) -> set:
    vocabulaire = set()
    corpus_train = read_conll("fr_sequoia-ud-train.conllu")
    for sentence in corpus_train.sentences:
        for token in sentence.tokens:
            vocabulaire.add(token.form)
    return vocabulaire


def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus, subcorpus: Optional[str]=None) -> Tuple[float, float]:
    nb_ok = 0  # nb de tokens correctement étiquetés
    nb_total = 0  # nb total de tokens dans les deux corpus
    oov_ok = 0  # nb tokens correctement étiquetés parmi les oov
    oov_total = 0  # nb tokens hors vocabulaire dans le corpus de référence.
    for sentence_gold, sentence_test in zip(
        corpus_gold.sentences, corpus_test.sentences
    ):
        # soit je veux que le sous-corpus soit je veux tout
        if subcorpus is None or subcorpus in sentence_gold.sent_id:
            for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
                assert (
                    token_gold.form == token_test.form
                )  # pose la condition que la forme du token du corpus_gold soit le même
                # que le corpus_test sinon lève une exception AssertionError
                if token_gold.tag == token_test.tag:
                    nb_ok += 1
                nb_total += 1
                if token_gold.is_oov:
                    oov_total += 1
                    if token_gold.tag == token_test.tag:
                        oov_ok += 1

    # taux d'exactitude global (nb_ok / nb_total) qui mesure
    # la précision globale de l'étiquetage de parties du discours
    # taux d'exactitude pour les tokens hors vocabulaire (oov_ok / oov_total)
    # qui mesure la précision de l'étiquetage des tokens hors vocabulaire
    return nb_ok / nb_total, oov_ok / oov_total


def compute_confusion_matrix(corpus_gold: Corpus, corpus_test: Corpus):
    y_true = []  # étiquettes réelles
    y_pred = []  # étiquettes prédites

    for sentence_gold, sentence_test in zip(
        corpus_gold.sentences, corpus_test.sentences
    ):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert token_gold.form == token_test.form

            # Collecte des étiquettes réelles et prédites
            y_true.append(token_gold.tag)
            y_pred.append(token_test.tag)

            # Matrice de confusion
            conf_matrix = confusion_matrix(y_true, y_pred)

            # Création d'un DataFramepour affficher la matrice de confusion avec les étiquettes
            labels = sorted(
                list(set(y_true + y_pred))
            )  # liste de toutes les étiquettes possible

            conf_df = pd.DataFrame(conf_matrix, index=labels, columns=labels)
            # ligne étiquette réelle
            # colonne étiquette prédites

    return conf_df

"""
The original sentences of the corpus are taken from:

French Europarl (sent_id prefix: Europar.550)
Wikipédia Fr (sent_id prefix: frwiki_50.1000)
Newspaper Est Républicain (sent_id prefix: annodis.er)
European Medicines Agency (sent_id prefix: emea-fr-dev and emea-fr-test)

se servir des sent_id pour séparer le corpus en 4 ?
"""



def main():
    model_spacy = spacy.load("fr_core_news_sm")

    vocabulaire = vocab_train("fr_sequoia-ud-train.conllu")

    corpus_gold = read_conll("fr_sequoia-ud-test.conllu", vocabulaire=vocabulaire)
    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    for subcorpus in ("annodis", "frwiki", "Europar", "emea-fr"):
        print(compute_accuracy(corpus_gold, corpus_test, subcorpus))
        print(compute_confusion_matrix(corpus_gold, corpus_test))


if __name__ == "__main__":
    time = timeit.timeit(
        main, number=1
    )  # éxecute la fonction main et affiche son temps d'xecution
    print(f"Le temps d'éxecution est égal à {time}")
