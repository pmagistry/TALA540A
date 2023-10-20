#!/usr/bin/env python
# coding: utf-8

"""
Ce fichier contient les fonctions pour évaluer la tokenisation des corpus
"""

from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datastructures import Corpus


def get_tags(ecorpus: Corpus, rcorpus: Corpus) -> tuple[list, list]:
    """
    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence

    Returns:
        tuple[list, list]: listes des pos du rcorpus et du ecorpus
    """
    # certains tags ne sont présents que dans un des deux corpus
    # 'etags' est une liste des pos présent dans le corpus à évaluer
    etags = []
    for esentence in ecorpus.sentences:
        for token in esentence.tokens:
            if token.pos not in etags:
                etags.append(token.pos)
    # 'rtags' est une liste des pos présent dans le corpus à évaluer
    rtags = []
    for rsentence in rcorpus.sentences:
        for token in rsentence.tokens:
            if token.pos not in rtags:
                rtags.append(token.pos)

    return etags, rtags


def get_accuracy(ecorpus: Corpus, rcorpus: Corpus) -> tuple[float, float]:
    """
    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence

    Returns:
        tuple[float, float]: accuracy de la tokenisation du ecorpus
                            avec et sans is_oov
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
        for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):
            assert etoken.form == rtoken.form
            # sans vocab
            total += 1
            if etoken.pos == rtoken.pos:
                acc += 1
            # avec vocab
            if rtoken.is_oov:
                total_oov += 1
                if etoken.pos == rtoken.pos:
                    acc_oov += 1

    return round(acc / total * 100, 2), round(acc_oov / total_oov * 100, 2)


def get_precision(ecorpus: Corpus, rcorpus: Corpus, tag: str) -> float:
    """
    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
        tag (str): un des tags du corpus à évaluer

    Returns:
        float: precision pour la classification du tag donné en argument
    """
    # 'all_positive' est le nb de docs attribués à la classe i
    all_positive = 0
    # 'true_positive' est le nb de docs correctement attribués à la classe i
    true_positive = 0
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences):
        for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):
            if etoken.pos == tag:
                all_positive += 1
            if etoken.pos == rtoken.pos and etoken.pos == tag:
                true_positive += 1
    return round(true_positive / all_positive * 100, 2)


def get_rappel(ecorpus: Corpus, rcorpus: Corpus, tag: str) -> float:
    """
    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
        tag (str): un des tags du corpus de référence

    Returns:
        float: rappel pour la classification du tag donné en argument
    """
    # 'all_positive' est le nb de docs appartenant à la classe i
    all_positive = 0
    # 'true_positive' est le nb de docs correctement attribués à la classe i
    true_positive = 0
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences):
        for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):
            if rtoken.pos == tag:
                all_positive += 1
            if etoken.pos == rtoken.pos and etoken.pos == tag:
                true_positive += 1
    return round(true_positive / all_positive * 100, 2)


def get_matrice(ecorpus: Corpus, rcorpus: Corpus):
    """fonction d'affichage des matrices de confusion
    pour la classification des pos

    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
    """
    # 'epos_rpos' est un dictionnaire (clé = rpos) de dictionnaire (clé = rpos)
    epos_rpos = defaultdict(lambda: defaultdict(int))
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences):
        for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):
            epos_rpos[etoken.pos][rtoken.pos] += 1

    # 'cm' est une matrice de confusion faite vec pandas
    cm = pd.DataFrame.from_dict(epos_rpos)
    # remplace les NaN par des 0 -> important pour les calculs après
    cm = cm.fillna(0)
    print("\n", cm)  # colonne rpos, ligne epos

    # on crée une matrice de confusion plus 'jolie' avec seaborn
    plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True)

    # titre du graphe et des axes
    plt.title("Matrice de confusion - données de test", fontsize=20, fontweight="bold")
    plt.xlabel("Etiquette prédite", fontsize=14)
    plt.ylabel("Etiquette correcte", fontsize=14)

    # affichage
    plt.show()
