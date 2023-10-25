from typing import List, Union, Dict, Set, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
#from pyJoules.energy_meter import measure_energy

@dataclass 
class Token():
    form: str
    tag: str
    is_oov: bool

@dataclass
class Sentence():
    #sent_id : str
    tokens: List[Token]

@dataclass
class Corpus():
    sentences: List[Sentence]


def read_conll(path: Path, vocabulaire : Optional[Set[str]]=None) -> Corpus:
    sentences = []    
    tokens = []
    vocab = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if "sent_id" in line :
                sent_id = line.split("=")[1].strip()
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

    return Corpus(sentences)

def build_vocabulaire(corpus: Corpus) -> Set[str]:
    return {tok.form for sent in corpus.sentences for tok in sent.tokens}

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


def compute_accuracy(corpus_gold: Corpus, corpus_test:Corpus, subcorpus: Optional[str] = None) -> float:
    nb_ok = 0
    nb_total = 0
    oov_ok = 0
    oov_total = 0
    vp = defaultdict(int)
    fp = defaultdict(lambda: defaultdict(int))
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        #if subcorpus is None or subcorpus in sentence_gold.sent_id:
            for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
                assert(token_gold.form == token_test.form)
                if token_gold.tag == token_test.tag:
                    vp[token_gold.tag] += 1
                    nb_ok += 1    
                    nb_total += 1
                else : 
                    nb_total += 1
                    fp[token_gold.tag][token_test.tag] += 1
                if token_gold.is_oov : 
                    oov_total += 1
                    if token_gold.tag == token_test.tag:
                        oov_ok += 1
    accuracy = nb_ok / nb_total
    oov = oov_ok / oov_total if oov_total != 0 else 0

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

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("gold", help = "gold", nargs = "?")
    parser.add_argument("test", help = "test", nargs = "?")
    
    return parser.parse_args()




    
def main():
    corpus_train = read_conll("fr_sequoia-ud-train.conllu")
    vocab_train = build_vocabulaire(corpus_train)

    model_spacy = spacy.load("fr_core_news_sm")
    corpus_gold = read_conll("fr_sequoia-ud-test.conllu", vocabulaire=vocab_train)
    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
   
    accuracy, oov, vp, fp = compute_accuracy(corpus_gold, corpus_test, vocab_train)
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

































