from typing import List, Union, Dict, Set, Optional
from pathlib import Path
from dataclasses import dataclass

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy

import timeit

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

def get_vocab(path:Path)-> Set[str]:
    vocabulaire = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#") and not line == "":
                fields = line.split("\t")
                if fields[0] != "-":
                    vocabulaire.add(fields[1])
    return vocabulaire


def read_conll(path: Path, vocabulaire: Optional[Set[str]]=None ) -> Corpus:
    sentences = []    
    tokens = []#objet token
    with open(path) as f:
        for line in f:
            line = line.strip()# retire les espaces debut et fin
            if not line.startswith("#"):
                
                if line == "":# si la ligne est vide = fin de phrase
                    sentences.append(Sentence(tokens))
                    tokens = []#formes, tag et oov, de nouveau vide pour la nouvelle phrase
                else:
                    fields = line.split("\t")
                    if not "-" in fields[0]:  # éviter les contractions type "du"
                        form, tag = fields[1], fields[3]
                        if vocabulaire is None:
                            is_oov=True
                        else:
                            is_oov = not form in vocabulaire
                        tokens.append(Token(form, tag, is_oov ))
    #print(Corpus(sentences))
    return Corpus(sentences)
# création de doc ? pour avoir des .token
def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)
#il fait l'inverse, on prend un doc pour en faire une phrase, prise en cpt de tokenisation
def doc_to_sentence(doc: SpacyDoc, origin: Sentence) -> Sentence:
    tokens = []
    for tok, origin_token in zip(doc, origin.tokens):
        tokens.append(Token(tok.text, tok.pos_, is_oov=origin_token.is_oov)) 
    return Sentence(tokens)

def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline ) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences)


def compute_accuracy(corpus_gold: Corpus, corpus_test:Corpus) -> float:
    nb_ok = 0
    nb_total = 0
    oov_ok = 0
    oov_total = 0
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert(token_gold.form == token_test.form)
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
    vocab_train = get_vocab("fr_sequoia-ud-train.conllu")
    corpus_gold = read_conll("fr_sequoia-ud-test.conllu",vocabulaire=vocab_train)

    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    print(compute_accuracy(corpus_gold, corpus_test))
    #ajouter timeit par là


if __name__ == "__main__":
    time=timeit.timeit(main,number=1)
    print(time)

































