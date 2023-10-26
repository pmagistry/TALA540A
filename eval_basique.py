from typing import List, Union, Dict, Set, Optional, Tuple
from collections import defaultdict
import regex
import sys
from pathlib import Path
from dataclasses import dataclass

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy

from pyJoules.energy_meter import measure_energy

from sklearn.metrics import classification_report

@dataclass
class Token:
    form: str
    tag: str
    is_oov: bool


@dataclass
class Sentence:
    tokens: List[Token]
    sentence_id: str


@dataclass
class Corpus:
    sentences: List[Sentence]
    corpus_id: str


def read_conll(path: Path, vocabulaire: Optional[Set[str]] = None, sous_corpus: bool = True) -> List[Corpus]:
    sentences: defaultdict(List[Sentence]) = defaultdict(list[Sentence])
    tokens: List[Token] = []
    corpus: List[Corpus] = []
    with open(path) as f:
        corp_id = ""
        for line in f:
            line = line.strip()
            if sous_corpus and line.startswith("# sent_id = "):
                sent_id = line[12:]    
                corp_id = regex.findall(r'^\w+',sent_id)[0]
            elif not line.startswith("#"):
                if line == "":
                    sentences[corp_id].append(Sentence(tokens, sent_id))
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
    all_corpus: List[Corpus] = []
    for c in sentences:
        corpus = Corpus(sentences[c], c)
        all_corpus.append(corpus)
        print("sous-corpus:", c)
    #return Corpus(sentences)
    return all_corpus


def build_vocabulaire(corpus: Corpus) -> Set[str]:
    return {tok.form for sent in corpus.sentences for tok in sent.tokens}


def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)


def doc_to_sentence(doc: SpacyDoc, origin: Sentence) -> Sentence:
    tokens = []
    for tok, origin_token in zip(doc, origin.tokens):
        tokens.append(Token(tok.text, tok.pos_ if len(tok.pos_) > 0 else tok.tag_, is_oov=origin_token.is_oov))
    return Sentence(tokens, "")

@measure_energy
def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences, "")


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

def print_report(corpus_gold: Corpus, corpus_test: Corpus):
    ref = [tok.tag for sent in corpus_test.sentences for tok in sent.tokens]
    test = [tok.tag for sent in corpus_gold.sentences for tok in sent.tokens]
    print(classification_report(ref, test))

def main():
    corpus_train = read_conll("data/fr_sequoia-ud-train.conllu", sous_corpus = False)[0]
    # False: un seul sous-corpus, pas de découpage
    vocab_train = build_vocabulaire(corpus_train)
    #for model_name in ("fr_core_news_sm", "fr_core_news_md", "fr_core_news_lg"):
    for model_name in ("spacy_model2/model-best/",):
        print(model_name)
        model_spacy = spacy.load(model_name)
        corpus_gold = read_conll("data/fr_sequoia-ud-test.conllu", vocabulaire=vocab_train, sous_corpus = True)
        for corpus_g in corpus_gold:
            print(corpus_g.corpus_id)
            corpus_test = tag_corpus_spacy(corpus_g, model_spacy)
            print(compute_accuracy(corpus_g, corpus_test))
            print_report(corpus_g, corpus_test)


if __name__ == "__main__":
    main()
