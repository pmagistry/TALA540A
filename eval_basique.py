from typing import List, Union, Dict, Set, Optional, Tuple
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
    sent_id: str
    tokens: List[Token]


@dataclass
class Corpus:
    sentences: List[Sentence]


def read_conll(path: Path, vocabulaire: Optional[Set[str]] = None) -> Corpus:
	lst_cat = []
	sentences: List[Sentence] = []
	tokens: List[Token] = []
	sid = ""
	with open(path) as f:
		for line in f:
			line = line.strip()
			if line.startswith("# genre =" ):
				sid = line.split(" ")[-1]
				if sid not in lst_cat : 
					lst_cat.append(sid)
			if not line.startswith("#"):
				if line == "":
					sentences.append(Sentence(sent_id=sid, tokens=tokens))
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
	return lst_cat, Corpus(sentences)


def build_vocabulaire(corpus: Corpus) -> Set[str]:
    return {tok.form for sent in corpus.sentences for tok in sent.tokens}


def sentence_to_doc(sentence: Sentence, vocab) -> SpacyDoc:
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)


def doc_to_sentence(doc: SpacyDoc, origin: Sentence) -> Sentence:
    tokens = []
    for tok, origin_token in zip(doc, origin.tokens):
        tag = tok.pos_ 
        if len(tag) == 0 :
            tag = tok.tag_
        tokens.append(Token(tok.text, tag, is_oov=origin_token.is_oov))
    return Sentence(origin.sent_id, tokens)

# @measure_energy
def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences)


def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus, subcorpus: Optional[str] = None) -> Tuple[float, float]:
    nb_ok = 0
    nb_total = 0
    oov_ok = 0
    oov_total = 0
    for sentence_gold, sentence_test in zip(
        corpus_gold.sentences, corpus_test.sentences
    ):
        if subcorpus is None or subcorpus in sentence_gold.sent_id: 
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
    lst_cat_train, corpus_train = read_conll("pl_lfg-ud-train.conllu")
    vocab_train = build_vocabulaire(corpus_train)
    for model_name in ("spacy_model_pl/model-best", "pl_core_news_sm", "pl_core_news_md", "pl_core_news_lg"):
        print(model_name)
        model_spacy = spacy.load(model_name)
        lst_cat_gold, corpus_gold = read_conll("pl_lfg-ud-test.conllu", vocabulaire=vocab_train)
        corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
        print(compute_accuracy(corpus_gold, corpus_test))
        for subcorpus in lst_cat_gold:
            print(subcorpus)
            print(compute_accuracy(corpus_gold, corpus_test, subcorpus))
        print_report(corpus_gold, corpus_test)


if __name__ == "__main__":
    main()
