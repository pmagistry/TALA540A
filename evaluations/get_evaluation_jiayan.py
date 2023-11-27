#!/usr/bin/env python
# coding: utf-8

"""
Ce fichier contient les fonctions pour évaluer le pos-tagging jiayan des corpus
"""

from typing import Optional
import regex
from datastructures import Corpus


def jiayan_sans(ecorpus: Corpus, rcorpus: Corpus) :
    """ print l'évaluation du posttagging 
    sans prendre en compte les sous-corpus
    
    Args:
        ecorpus (Corpus): corpus du modèle à évaluer
        rcorpus (Corpus): corpus de référence
    """
    
    print(f"\nPour le corpus {ecorpus.name} :")
    # on va chercher l'accuracy
    acc = get_accuracy(ecorpus, rcorpus)
    print(f"L'accuracy avec notre modèle est à {acc[0]}%.")
    print(f"En tenant compte du vocabulaire, l'accuracy est à {acc[1]}%.")


def get_accuracy(ecorpus: Corpus, rcorpus: Corpus, subcorpus: Optional[str] = None) -> tuple[float, float]:
    """
    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
        subcorpus (Optional[str]): nom du sous-corpus du corpus test à évaluer

    Returns:
        tuple[float, float]: accuracy de la tokenisation du ecorpus avec et sans is_oov
    """
    
    # 'total' est le nb total de docs classés
    total = 0
    # 'total_oov' est le nb total de docs classés avec is_oov == True
    total_oov = 0
    
    # 'acc' est le nb de docs bien classés
    acc = 0
    # 'acc' est le nb de docs bien classés avec is_oov == True
    acc_oov = 0
    
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences):
        if subcorpus is None:
            for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):
                assert etoken.form == rtoken.form
                # sans vocab
                total += 1
                if etoken.pos == rtoken.pos:
                    acc += 1
                # avec vocab
                if etoken.is_oov:
                    total_oov += 1
                    if etoken.pos == rtoken.pos:
                        acc_oov += 1
        else:
            if rsentence.sent_id == subcorpus :
                for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):
                    assert etoken.form == rtoken.form
                    # sans vocab
                    total += 1
                    acc += tableau_conversion(etoken.pos, rtoken.pos) # renvoie 1 ou 0
                    # avec vocab
                    if etoken.is_oov:
                        total_oov += 1
                        acc += tableau_conversion(etoken.pos, rtoken.pos) # renvoie 1 ou 0

    return round(acc / total * 100, 2), round(acc_oov / total_oov * 100, 2)


def tableau_conversion(epos: str, rpos: str) -> int:
    result = 0
    if rpos == "ADJ" and regex.match(r"a|m", epos):
        result = 1
    elif rpos == "DET" and regex.match(r"r|b", epos):
        result = 1
    elif regex.match(r"CCONJ|SCONJ", rpos) and epos == "c" :
        result = 1
    elif rpos == "ADV" and regex.match(r"d|h", rpos) :
        result = 1
    elif rpos == "INTJ" and epos == "e" :
        result = 1
    elif rpos == "NUM" and epos == "m" :
        result = 1
    elif rpos == "NOUN" and regex.match(r"q|n|ni|nl|nt|h", epos) :
        result = 1
    elif rpos == "PROPN" and regex.match(r"nh|ns|nz|z", epos) :
        result = 1
    elif rpos == "ADP" and regex.match(r"nd|p|k", epos) :
        result = 1
    elif rpos == "PRON" and epos == "r" :
        result = 1
    elif rpos == "AUX" and regex.match(r"u|v", epos) :
        result = 1
    elif rpos == "PART" and regex.match(r"u|k", epos) :
        result = 1
    elif rpos == "VERB" and epos == "v":
        result = 1
    elif regex.match(r"PUNCT|SYM", rpos) and epos == "wp" :
        result = 1
    
    # base on context/token : i, j tester en ne les prenant pas en compte et en mettant +1 peu importe
    # pas présent ni dans train ni dans test : o, g, x, ws
    
    return result


def test_tokens(ecorpus: Corpus, rcorpus: Corpus):
    """fonction d'affichage pour voir les résultats obtenus
        après l'obtention des corpus

    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
    """
    # pour voir sur le trcorpus: Corpuserminal la tokenisation des deux corpus
    print("etoken", "\t", "rtoken")
    for esentences, rsentences in zip(ecorpus.sentences, rcorpus.sentences):
        for etoken, rtoken in zip(esentences.tokens, rsentences.tokens):
            # plusieurs proposition aux choix en fonction de ce que l'on veut voir
            # print(etoken, "\t", rtoken)
            # if etoken.pos != rtoken.pos:
                # print(etoken, "\t", rtoken)
                # print(etoken.form, "\t", rtoken.form)
                # print(etoken.pos, "\t", rtoken.pos)
                
            if tableau_conversion(etoken.pos, rtoken.pos) == 0:
                print(etoken.form, etoken.pos, "\t", rtoken.form, rtoken.pos)
            # if regex.match(r"wp", etoken.pos):
            #     print(etoken.form, etoken.pos, "\t", rtoken.form, rtoken.pos)