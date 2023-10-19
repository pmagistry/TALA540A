from typing import List, Set, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy

from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns


######################
# DATACLASS
######################
@dataclass
class Token:
    form: str
    tag: str
    is_oov: bool


@dataclass
class Sentence:
    tokens: List[Token]


@dataclass
class Corpus:
    sentences: List[Sentence]


########################
# création du corpus
########################
def read_conll(path: Path, vocabulaire: Optional[Set[str]] = None) -> Corpus:
    sentences = []
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
                    if not "-" in fields[0]:  # éviter les contractions type "du"
                        if vocabulaire is None:
                            is_oov = True
                        else:
                            is_oov = (
                                not form in vocabulaire
                            )  # même chose que False if form in vocabulaire
                        tokens.append(Token(form, tag, is_oov))
    return Corpus(sentences)


#########################
# extraction vocabulaire
#########################
def vocab_extrac(path: Path) -> set:
    vocabulaire = set()
    corpus_train = read_conll(path)
    for sentence in corpus_train.sentences:
        for token in sentence.tokens:
            vocabulaire.add(token.form)
    return vocabulaire


##################################
# passage de Sentence à Doc spacy
##################################
def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)


#####################################
# passage de Doc spacy à Sentence
#####################################
def doc_to_sentence(doc: SpacyDoc, origin: Sentence) -> Sentence:
    tokens = []
    for tok, origin_token in zip(doc, origin.tokens):
        tokens.append(Token(tok.text, tok.pos_, is_oov=origin_token.is_oov))
    return Sentence(tokens)


##################################
# tag d'un Corpus avec spacy
##################################
def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences)


#########################################
# calcul de l'accuracy entre deux corpus
#########################################
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
            if token_test.is_oov:
                oov_total += 1
                if token_gold.tag == token_test.tag:
                    oov_ok += 1
    return nb_ok / nb_total, oov_ok / oov_total


def make_confusion_matrix(corpus_gold: Corpus, corpus_test: Corpus):
    tag_true = []
    tag_pred = []
    for sentence_gold, sentence_test in zip(
        corpus_gold.sentences, corpus_test.sentences
    ):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            tag_true.append(token_gold.tag)
            tag_pred.append(token_test.tag)
    return confusion_matrix(tag_true, tag_pred)

def beautiful_confusion_matrix(confusion_matrix) -> None:
    # création d'une figure et d'un axe pour le graphique
    # f, ax = plt.subplots(figsize=(8,6))

    # création d'une heatmap pour visualiser la matrice de confusion
    sns.heatmap(confusion_matrix,
                annot=True,
                cmap="Blues",
                robust=True,
                linewidth=1)

    # titre du graphique et étiquettes des axes
    plt.title("Matrice de confusion - données de test", fontsize=20, fontweight="bold")
    plt.xlabel("Etiquette prédite", fontsize=14)
    plt.ylabel("Etiquette correcte", fontsize=14)

    # sauvegarde matrice
    plt.savefig('confusion_matrix.svg')


#######
# MAIN
#######
def main():
    model_spacy = spacy.load("fr_core_news_sm")
    print("Modèle spacy chargé !")

    vocabulaire = vocab_extrac(Path("DATA/fr_sequoia-ud-train.conllu"))

    corpus_gold = read_conll(
        Path("DATA/fr_sequoia-ud-test.conllu"), vocabulaire=vocabulaire
    )

    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    # print(compute_accuracy(corpus_gold, corpus_test))

    cm = make_confusion_matrix(corpus_gold=corpus_gold, corpus_test=corpus_test)
    beautiful_confusion_matrix(cm)


if __name__ == "__main__":
    main()
