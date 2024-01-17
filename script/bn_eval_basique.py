from collections import defaultdict
from itertools import islice
from typing import List, Union, Dict, Set, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from sklearn.preprocessing import LabelEncoder
from spacy import Language as SpacyPipeline
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc
import spacy
from pyJoules.energy_meter import measure_energy
from sklearn.metrics import classification_report
from pprint import pprint
from boostsa import Bootstrap
import pos_tagging_with_banglanltk
import extract_train_corpus

'''
Nécessite: 
1. sudo chmod -R a+r /sys/class/powercap/intel-rapl
2. Essai adaptation Spacy , mais avec modèle entraîné par hindi
'''

@dataclass
class Token:
    form: str # transliteration 
    tag: str
    is_oov: bool


@dataclass
class Sentence:
    sent_id: str
    tokens: List[Token] # transliteration


@dataclass
class Corpus:
    sentences: List[Sentence]

# lecture fichier conllu
def read_conll(path: Path, vocabulaire: Optional[Set[str]] = None) -> Corpus:
    sentences: List[Sentence] = []
    tokens: List[Token] = []
    sid = ""
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("# sent_id =" ):
                sid = line.split(" ")[-1]
            if not line.startswith("#"):
                if line == "": # nouvelle phrase
                    sentences.append(Sentence(sent_id=sid, tokens=tokens))
                    tokens = [] # resetting tokens
                else:
                    fields = line.split("\t")
                    make_form = [item for item in fields[9].split("|") if item.startswith("Translit=")]
                    
                    form, tag = make_form[0][9:], fields[3] # form -"Translit="
                    if not "-" in fields[0]:  # éviter les contractions type "du"
                        if vocabulaire is None:
                            is_oov = True
                        else:
                            is_oov = not form in vocabulaire
                        tokens.append(Token(form, tag, is_oov))
    return Corpus(sentences)

# vocabulaire
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

# sudo chmod -R a+r /sys/class/powercap/intel-rapl
@measure_energy
def tag_corpus_spacy(corpus: Corpus, model_spacy: SpacyPipeline) -> Corpus:
    sentences = []
    for sentence in corpus.sentences:
        doc = sentence_to_doc(sentence, model_spacy.vocab)
        doc = model_spacy(doc)
        sentences.append(doc_to_sentence(doc, sentence))
    return Corpus(sentences)

# calcul accuracy
def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus, subcorpus: Optional[str] = None) -> Tuple[float, float]:
    nb_ok = 0
    nb_total = 0
    oov_ok = 0
    oov_total = 0
    for sentence_gold, sentence_test in zip(
        corpus_gold.sentences, corpus_test.sentences):
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

# Impression du classification report
def print_report(corpus_gold: Corpus, corpus_test: Corpus):
    ref = [tok_gold.tag for sent_gold, sent_test in zip(corpus_gold.sentences, corpus_test.sentences)
           for tok_gold, tok_test in zip(sent_gold.tokens, sent_test.tokens)]
    
    test = [tok_test.tag for sent_gold, sent_test in zip(corpus_gold.sentences, corpus_test.sentences)
            for tok_gold, tok_test in zip(sent_gold.tokens, sent_test.tokens)]
    print(classification_report(ref, test, zero_division=0)) # print
    
    
# AFFICHAGE DE SCORE # 
def get_scores(corpus_gold):
    bootstrap = Bootstrap() ###
    targets = [tok.tag for sent in corpus_gold.sentences for tok in sent.tokens]
    encoder = LabelEncoder().fit(targets)
    targets = encoder.transform(targets)    
    outcomes = {}
    for model_name in ("../output/model-best", "xx_sent_ud_sm", "xx_ent_wiki_sm"):         
        model_spacy = spacy.load(model_name)
        corpus_test = tag_corpus_spacy(corpus_gold, model_spacy)
        try: 
            outcomes[model_name] = encoder.transform([tok.tag for sent in corpus_test.sentences for tok in sent.tokens])
            print(compute_accuracy(corpus_gold, corpus_test, None))
            print_report(corpus_gold, corpus_test)
        except ValueError as e :
            print(e)
        try :
            bootstrap.test(targets, outcomes['../output/model-best'], outcomes['xx_sent_ud_sm'], outcomes['xx_ent_wiki_sm'], \
                            "H0", "H1",sample_size=.5, n_loops=500, verbose=True)
        except KeyError as e:
            print(e)
            
    
    
 
def main():
    print("Veuillez noter que le programme nécéssite la commande suivante pour pyJoules :\
            sudo chmod -R a+r /sys/class/powercap/intel-rapl \nEn cours de traitement...")
    
    try: 
    
        ### 1. Spacy Model comparison  bn et hindi 
    
        corpus_train_hi = read_conll("../corpus/hindi/hi_hdtb-ud-train.conllu")
        vocab_train = build_vocabulaire(corpus_train_hi)
        corpus_gold_bn= read_conll("../corpus/bengali/bn_bru-ud-test.conllu", vocabulaire=vocab_train)
        get_scores(corpus_gold_bn)
        
        
        ## 2. Train with corpus nltr
        
        corpus_train_nltr = extract_train_corpus.read_nltr_corpus('../corpus/bengali/bn_nltr_pos_corpus.txt')
        vocab = build_vocabulaire(corpus_train_nltr)
        corpus_gold2 = read_conll("../corpus/bengali/bn_bru-ud-test.conllu", vocabulaire=vocab)
        get_scores(corpus_gold2)

        
        ### 3. banglanltk 
        corpus_train_banglanltk = pos_tagging_with_banglanltk.format_banglanltk_pos('../corpus/bengali/bn_connll_txt.txt')
        vocab3 = build_vocabulaire(corpus_train_banglanltk)
        corpus_gold3 = read_conll("../corpus/bengali/bn_bru-ud-test.conllu", vocabulaire=vocab3)
        get_scores(corpus_gold3)
        
        
        
        ### 3.  BNLP   #########
        corpus_train_bnlp = pos_tagging_with_banglanltk.format_bnlp_pos('../corpus/bengali/bn_connll_txt.txt')
        vocab4= build_vocabulaire(corpus_train_bnlp)
        corpus_gold4 = read_conll("../corpus/bengali/bn_bru-ud-test.conllu", vocabulaire=vocab4)
        get_scores(corpus_gold4)
    except Exception as e:
        print(e)
        pass
    
            
              
       
if __name__ == "__main__":
    main()


