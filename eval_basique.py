from typing import List, Union, Dict
from pathlib import Path
from dataclasses import dataclass

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy

@dataclass 
class Token():
    form: str
    tag: str

@dataclass
class Sentence():
    tokens: List[Token]

@dataclass
class Corpus():
    sentences: List[Sentence]


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
                    if not "-" in fields[0]: # éviter les contractions type "du"
                        tokens.append(Token(form, tag))
    return Corpus(sentences)

def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline ) -> Corpus:
    pass


def compute_accuracy(corpus_gold: Corpus, corpus_test:Corpus) -> float:
    nb_ok = 0
    nb_total = 0
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert(token_gold.form == token_test.form)
            if token_gold.tag == token_test.tag:
                nb_ok += 1
            nb_total += 1
    return nb_ok / nb_total




def main():
    corpus_gold = read_conll("fr_sequoia-ud-test.conllu")
    print(compute_accuracy(corpus_gold, corpus_gold))


if __name__ == "__main__":
    main()

































