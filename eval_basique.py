"""
Vocab a creer à partir du corpus train
A partir de là , voir si token rencontrée out of domain OOV
A compléter

2. séparation corpus ud fr sequoi, medical, news, non-fiction, wiki


"""


from typing import List, Union, Dict, Set, Optional
from pathlib import Path
from dataclasses import dataclass

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy
from pyJoules.energy_meter import measure_energy
import regex


@dataclass
class Token:
    form: str
    tag: str
    is_oov: bool


@dataclass
class Sentence:
    tokens: List[Token]
    sent_id: str


@dataclass
class Corpus:
    sentences: List[Sentence]


# create vocab -> correct
def get_vocab(corpus: Corpus) -> Set[str]:
    words = [ tok.form for sents in corpus.sentences for tok in sents.tokens ] 
    # try and reverse
    vocab = SpacyDoc(words)  #(expected spacy.vocab.Vocab, got list)
    return SpacyDoc(vocab, words=words)


# split
def TypeSplit(path: Path) -> List[Dict]:
    # get id of big corpus -> split (-) -> if starts with emea, frwiki, annodis , Europarwith open(path) as f:
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                line = line.split()

                if line[1].startswith("sent_id"):
                    id = line[3].rsplit("_")
                    # spaced_line = list(regex.split(r' ', line, maxsplit=0, flags=0))
                    # id = list(regex.split(r'\p{P}', id, maxsplit=0, flags=0))

                    id = id[-1]

    pass


def read_conll(path: Path, vocabulaire: Optional[Set[str]] = None) -> Corpus:
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
                    if not "-" in fields[0]:  # éviter les contractions type "du"
                        if vocabulaire is None:
                            is_oov = True
                        else:
                            is_oov = not form in vocabulaire
                        tokens.append(Token(form, tag, is_oov))
            # adding portion to get beginning of lines

    return Corpus(sentences)


def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)


def doc_to_sentence(doc: SpacyDoc, origin: Sentence) -> Sentence:
    tokens = []
    for tok, origin_token in zip(doc, origin.tokens):
        tokens.append(Token(tok.text, tok.pos_, is_oov=origin_token.is_oov))
    return Sentence(tokens)


def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences)


def compute_accuracy(
    corpus_gold: Corpus, corpus_test: Corpus, subcorpus: Optional[str]
) -> float:
    nb_ok = 0
    nb_total = 0
    oov_ok = 0
    oov_total = 0
    for sentence_gold, sentence_test in zip(
        corpus_gold.sentences, corpus_test.sentences
    ):
        if subcorpus is None or subcorpus in sentence_gold.sents_id:
            for token_gold, token_test in zip(
                sentence_gold.tokens, sentence_test.tokens
            ):
                assert token_gold.form == token_test.form
                if token_gold.tag == token_test.tag:
                    nb_ok += 1
                nb_total += 1
                if token_gold.is_oov:
                    oov_total += 1
                    if token_gold.tag == token_test.tag:
                        oov_ok += 1

    return nb_ok / nb_total, oov_ok / oov_total


def main():
    model_spacy = spacy.load("fr_core_news_sm")
    corpus_gold = read_conll("corpus/fr_sequoia-ud-test.conllu")

    # vocab = get_vocab(read_conll('corpus/fr_sequoia-ud-train.conllu'))

    # print(corpus_gold)

    # corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    # print(compute_accuracy(corpus_gold, corpus_test))


def print_report():
    pass


if __name__ == "__main__":
    main()
