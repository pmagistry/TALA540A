from typing import List, Union, Dict, Set
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy
import matplotlib.pyplot as plt
import seaborn as sns


@dataclass 
class Token():
    form: str
    tag: str
    is_oov: bool

@dataclass
class Sentence():
    tokens: List[Token]

@dataclass
class Corpus():
    sentences: List[Sentence]


def read_conll(path: Path, vocabulaire : [set[str]]=None) -> Corpus:
    sentences = []    
    tokens = []
    vocab = set()
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
                       # tokens.append(Token(form, tag))
                        if vocabulaire is None : 
                            is_oov = True
                        else : 
                            is_oov = False 
                        tokens.append(Token(form,tag,is_oov))
                        vocab.add(form)

    return Corpus(sentences), vocab

def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)

def doc_to_sentence(doc: SpacyDoc) -> Sentence:
    tokens = []
    for tok in doc:
        tokens.append(Token(tok.text, tok.pos_, is_oov=tok.is_oov)) # bof
    return Sentence(tokens) 

def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline ) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc))
    return Corpus(sentences)


def compute_accuracy(corpus_gold: Corpus, corpus_test:Corpus, vocabulaire) -> float:
    nb_ok = 0
    nb_total = 0
    oov_total = 0
    vp = defaultdict(int)
    fp = defaultdict(lambda: defaultdict(int))
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            assert(token_gold.form == token_test.form)
            if token_gold.tag == token_test.tag:
                vp[token_gold.tag] += 1
                nb_ok += 1
            nb_total += 1
            if token_test.form not in vocabulaire : # est ce que ce token est un oov étant donné le vocabulaire du train
                oov_total += 1
                fp[token_gold.tag][token_test.tag] += 1
    accuracy = nb_ok / nb_total
    oov = oov_total / len(vocabulaire)

    return accuracy, oov, vp, fp


def generate_confusion_matrix(VP, FP):
    all_tags = list(set(VP.keys()).union(FP.keys()))
    confusion_matrix = pd.DataFrame(0, index=all_tags, columns=all_tags, dtype=int)


    for tag, count in VP.items():
        confusion_matrix.at[tag, tag] = count

    for real_tag, pred_tags in FP.items():
        for pred_tag, count in pred_tags.items():
            confusion_matrix.at[real_tag, pred_tag] = count

    return confusion_matrix




def main():
    model_spacy = spacy.load("fr_core_news_sm")
    corpus_gold, vocab = read_conll("fr_sequoia-ud-test.conllu")

    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    accuracy, oov, vp, fp = compute_accuracy(corpus_gold, corpus_test, vocab)
    print("accuracy : " , accuracy)
    print("OOV : ", oov )
    
    
    
    confusion_data = generate_confusion_matrix(vp, fp)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(confusion_data, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Real")
    plt.title("Matrice de confusion")
    plt.show()

    


if __name__ == "__main__":
    main()

































