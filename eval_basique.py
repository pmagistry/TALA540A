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


def read_conll(path: Path, vocabulaire: Optional[Set[str]]=None ) -> Corpus:
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
                        if vocabulaire is None:
                            is_oov=True
                        else:
                            is_oov = not form in vocabulaire
                        tokens.append(Token(form, tag, is_oov ))
    return Corpus(sentences)

def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)

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
    actual = []
    predicted = []
    nb_ok = 0
    nb_total = 0
    oov_ok = 0
    oov_total = 0
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert(token_gold.form == token_test.form)
            if token_gold.tag == token_test.tag:
                nb_ok += 1
                actual.append(1)
            else:
                actual.append(0)
            nb_total += 1
            predicted.append(1)
            if token_gold.is_oov:
                oov_total += 1
                if token_gold.tag == token_test.tag:
                    oov_ok += 1
    matrice(actual, predicted)
    return nb_ok / nb_total, oov_ok / oov_total

def matrice(actual, predicted):
   from sklearn import metrics
   import matplotlib.pyplot as plt
   confusion_matrix = metrics.confusion_matrix(actual, predicted)
   cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
   cm_display.plot()
   plt.show()

   """
   ou pour simplement imprimer la matrice : 
   from sklearn.metrics import confusion_matrix
    matrix = confusion_matrix(y_true=actual, y_pred=predicted)
    print(matrix)"""



def main():
    model_spacy = spacy.load("fr_core_news_sm")
    corpus_gold = read_conll("fr_sequoia-ud-test.conllu")
    corpus_train = read_conll("fr_sequoia-ud-train.conllu")
    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    print(compute_accuracy(corpus_gold, corpus_test))


if __name__ == "__main__":
    temps_execution = timeit.timeit(main, number=1)
    print(temps_execution)
    #main()
    


































