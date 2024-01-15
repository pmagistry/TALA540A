#!/usr/bin/env python
# coding: utf-8

"""
Ce fichier contient les fonctions pour évaluer le pos-tagging spacy des corpus
"""

from collections import OrderedDict
from typing import Optional
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datastructures import Corpus


def spacy_avec(ecorpus: Corpus, rcorpus: Corpus) :
    """ print l'évaluation du posttagging 
    en prenant en compte les sous-corpus
    
    Args:
        ecorpus (Corpus): corpus du modèle à évaluer
        rcorpus (Corpus): corpus de référence
    """
    
    print(f"\nPour le corpus {ecorpus.name} :")
    # pour chaque sous-corpus
    for subcorpus in {sentence.sent_id for sentence in rcorpus.sentences}:   
        print(f"Pour le sous-corpus {subcorpus} :")
        # on va chercher l'accuracy   
        acc = get_accuracy(ecorpus, rcorpus, subcorpus)
        print(f"L'accuracy avec notre modèle est à {acc[0]}%.")
        print(f"En tenant compte du vocabulaire, l'accuracy est à {acc[1]}%.")
        # et ensuite la matrice de confusion
        print("\nLa matrice de confusion, sans tenir compte du vocabulaire.")
        get_matrice(ecorpus, rcorpus, subcorpus)
    
    
def spacy_sans(ecorpus: Corpus, rcorpus: Corpus) :
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
    # et ensuite la matrice de confusion
    print("\nLa matrice de confusion, sans tenir compte du vocabulaire.")
    get_matrice(ecorpus, rcorpus)


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
                    if etoken.pos == rtoken.pos:
                        acc += 1
                    # avec vocab
                    if etoken.is_oov:
                        total_oov += 1
                        if etoken.pos == rtoken.pos:
                            acc_oov += 1

    return round(acc / total * 100, 2), round(acc_oov / total_oov * 100, 2)


def get_matrice(ecorpus: Corpus, rcorpus: Corpus, subcorpus: Optional[str] = None):
    """fonction d'affichage des matrices de confusion
    pour la classification des pos

    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
    """
    
    # 'etags' contient les tags du corpus à évaluer
    etags = {token.pos for sentence in ecorpus.sentences for token in sentence.tokens}
    # 'rtags' contient les tags du corpus de référence
    rtags = {token.pos for sentence in rcorpus.sentences for token in sentence.tokens}
    tags = etags.union(rtags)

    # 'epos_rpos' est un dictionnaire (clé = etag) de dictionnaire (clé = rtag)
    epos_rpos = OrderedDict()
    for etag in tags: # tag du modèle à évaluer
        epos_rpos[etag] = OrderedDict()
        for rtag in tags: # tag du corpus de référence
            epos_rpos[etag][rtag] = 0

    # on prend en compte les sous-corpus ou non en fonction
    # du paramètres 'subcorpus'
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences):
        if subcorpus is None:
            for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):   
                epos_rpos[etoken.pos][rtoken.pos] += 1    
        else:
            if rsentence.sent_id == subcorpus :
                for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):
                    epos_rpos[etoken.pos][rtoken.pos] += 1

    # 'cm' est une matrice de confusion faite avec pandas
    cm = pd.DataFrame.from_dict(epos_rpos)

    # remplace les NaN par des 0 -> important pour les calculs après
    cm = cm.fillna(0)
    print("\n", cm)  # colonne rpos, ligne epos

    # on crée une matrice de confusion plus 'jolie' avec seaborn
    plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, fmt=".1f", annot=True)

    # titre du graphe et des axes
    plt.title("Matrice de confusion - données de test", fontsize=20, fontweight="bold")
    plt.xlabel("Etiquette prédite", fontsize=14)
    plt.ylabel("Etiquette correcte", fontsize=14)

    # affichage
    plt.show()