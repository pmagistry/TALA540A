from typing import List, Union, Dict, Set, Optional
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict

from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

@dataclass 
class Token():
    form: str
    tag: str
    is_oov : bool

@dataclass
class Sentence():
    tokens: List[Token]

@dataclass
class Corpus():
    sentences: List[Sentence]


def read_conll(path: Path, vocabulaire : Optional[set[str]]=None) -> Corpus:
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
                        if vocabulaire is None :
                            is_oov = True
                        else:
                            is_oov = not form in vocabulaire
                        tokens.append(Token(form, tag, is_oov))
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
            if token_gold.is_oov :
                oov_total += 1
                if token_gold.tag == token_test.tag:
                    oov_ok += 1
                    
    return nb_ok / nb_total, oov_ok / oov_total

# Matrice de confusion
"""
def confusion_matrix(corpus_gold: Corpus, corpus_test: Corpus) -> str:
    confusion_matrix = defaultdict(lambda: defaultdict(int))

    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            actual_tag = token_test.tag
            predicted_tag = token_gold.tag
            
            if actual_tag == predicted_tag:
                confusion_matrix[actual_tag]['TP'] += 1
            else:
                confusion_matrix[actual_tag]['FN'] += 1
                confusion_matrix[predicted_tag]['FP'] += 1

    return confusion_matrix
"""
def plot_confusion_matrix(true_labels, predicted_labels, classes):
    cm = confusion_matrix(true_labels, predicted_labels)

    plt.figure(figsize=(8, 6))
    sns.set(font_scale=1.2)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, xticklabels=classes, yticklabels=classes)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()
    
    
def main():
    model_spacy = spacy.load("fr_core_news_sm")
    corpus_gold = read_conll("corpus/corpus_eval/fr_sequoia-ud-test.conllu")

    corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
    #print(compute_accuracy(corpus_gold, corpus_test))
    
    """  
    accuracy, oov_accuracy = compute_accuracy(corpus_gold, corpus_test)
    matrix = confusion_matrix(corpus_gold, corpus_test)

    print(f"Overall Accuracy: {accuracy * 100:.2f}%")
    print(f"OOV Accuracy: {oov_accuracy * 100:.2f}%")

    # Print the confusion matrix 
    print("\nConfusion Matrix:")
    for tag, counts in matrix.items():
        print(f"Tag: {tag}")
        print(f"  True Positives: {counts['TP']}")
        print(f"  False Positives: {counts['FP']}")
        print(f"  False Negatives: {counts['FN']}")
        precision = counts['TP'] / (counts['TP'] + counts['FP']) if counts['TP'] + counts['FP'] > 0 else 0
        recall = counts['TP'] / (counts['TP'] + counts['FN']) if counts['TP'] + counts['FN'] > 0 else 0
        f1_score = (2 * precision * recall) / (precision + recall) if precision + recall > 0 else 0
        print(f"  Precision: {precision * 100:.2f}%")
        print(f"  Recall: {recall * 100:.2f}%")
        print(f"  F1 Score: {f1_score * 100:.2f}%")
        print()
    """
    # Matrice de confusion
    true_labels = []
    predicted_labels = []

    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens):
            true_labels.append(token_gold.tag)
            predicted_labels.append(token_test.tag)

    classes = list(set(true_labels))

    # Print confusion matrix
    print("Confusion Matrix:")
    cm = confusion_matrix(true_labels, predicted_labels)
    print(cm)

    # Print classification report
    report = classification_report(true_labels, predicted_labels)
    print("\nClassification Report:")
    print(report)

    # Plot the confusion matrix using the function
    plot_confusion_matrix(true_labels, predicted_labels, classes)


if __name__ == "__main__":
    main()