"""
Ce script permet de tester l'annotation automatique en pos à partir de fichiers conll
"""

import argparse
import re
from pathlib import Path
from typing import Set, Tuple, Optional, List

import spacy
from datastructures import Token, Sent, Corpus
from sklearn.metrics import confusion_matrix
from spacy import Language as SpacyPipeline
from spacy.tokens import Doc as SpacyDoc


###### Argparse
def arguments() -> argparse.ArgumentParser:
    """
    Initialise nos arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("gold", help="fichier texte ou conll")
    parser.add_argument("ref", help="fichier texte ou conll", nargs="?")
    return parser.parse_args()


##### Read Conll
def read_conll(path: Path, vocab: Optional[Set[str]] = None) -> Tuple[Corpus, Set[str]]:
    """
    Lit un fichier conll et le formate dans une classe corpus
    path : lien Path vers le fichier conll 
    vocab : un dictionnaire de vocabulaire 
    renvoie une valeur de classe Corpus 
    """

    sentences: List[Sent] = []
    tokens: List[Token] = []
    vocabulary = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# sent_id"):
                # On récupère le nom
                sent_id = re.findall(r"# sent_id = (.*)_.*", line)
                # print(id)
            if not line.startswith("#"):
                if line == "":
                    sentences.append(Sent(sent_id[0], tokens))
                    tokens = []
                else:
                    fields = line.split("\t")
                    form, pos = fields[1], fields[3]
                    vocabulary.add(form)
                    if not "-" in fields[0]:  # éviter les contractions type "du"
                        if vocab is None:
                            is_oov = True
                        else:
                            is_oov = not form in vocab
                        tokens.append(Token(form, pos, is_oov))
    return Corpus(sentences), vocabulary


####### Création des corpus de test


def sentence_to_doc(sentence: List[Token], vocab) -> SpacyDoc:
    """
    transforme une liste de tokens en classe SpacyDoc
    """
    words = [tok.form for tok in sentence]
    return SpacyDoc(vocab, words=words)


def doc_to_sentence(sent_id: str, doc: SpacyDoc, origin: Sent) -> Sent:
    """
    Transforme des classes SpacyDoc en classe Sent
    """
    tokens = []
    for tok, origin_tok in zip(doc, origin.tokens):
        tokens.append(Token(tok.text, tok.pos_, is_oov=origin_tok.is_oov))
    return Sent(sent_id, tokens)


def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline) -> Corpus:
    """
    Transforme l'annotation de spacy en classe Corpus pour comparer avec
    les fichiers conll
    """
    sentences = []
    # print([sent for sent in corpus.sents])
    for sentence in corpus.sents:
        doc = sentence_to_doc(sentence.tokens, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(sentence.sent_id, doc, sentence))
    return Corpus(sentences)


####### Calcul de la précision
def compute_accuracy(
    gold_list: Corpus,
    test_list: Corpus,
    subcorpus: Optional[str] = None,
    confusion: Optional[bool] = False,
) -> Tuple[float, float]:
    """
    Permet de calculer l'exactitude d'annotation d'un corpus de test
    par rapport à un corpus de référence
    Peut être fait par sous-corpus
    Peut sortir une matrice de confusion
    """
    correct = 0
    total = 0
    oov_total = 0
    oov_ok = 0

    if confusion:
        y_gold = []
        y_pred = []

    for gold_sentence, test_sentence in zip(gold_list.sents, test_list.sents):
        if subcorpus is None or subcorpus in gold_sentence.sent_id:
            for gold_token, test_token in zip(
                gold_sentence.tokens, test_sentence.tokens
            ):
                assert gold_token.form == test_token.form
                if confusion:
                    y_gold.append(gold_token.pos)
                    y_pred.append(test_token.pos)
                total += 1
                if gold_token.pos == test_token.pos:
                    correct += 1
                if gold_token.is_oov:
                    oov_total += 1
                    if gold_token.pos == test_token.pos:
                        oov_ok += 1

            if confusion:
                print(confusion_matrix(y_gold, y_pred))

    return correct / total, oov_ok / oov_total


if __name__ == "__main__":
    #### lecture de notre corpus conll
    args = arguments()

    if args.ref:
        if args.ref.endswith(".conllu"):
            corpus_ref, vocab_ref = read_conll(args.ref)

    if args.gold.endswith(".conllu"):
        corpus_gold, vocab_gold = read_conll(args.gold, vocab_ref)

    spacy_model = spacy.load("fr_core_news_sm")
    corpus_test = tag_corpus_spacy(corpus_gold, spacy_model)

    subcorp = set()
    for sub in corpus_test.sents:
        subcorp.add(sub.sent_id)
    print(subcorp)

    for sub in subcorp:
        accur, accur_oov = compute_accuracy(corpus_gold, corpus_test, sub)

        print(
            f"------ {sub} ------\
            \nPrécision du pos tagging : {round(accur, 2)}\
            \nPrécision sur OOV : {round(accur_oov, 2)}"
        )
