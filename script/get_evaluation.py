#!/usr/bin/env python
# coding: utf-8

"""
Ce fichier contient les fonctions pour évaluer la tokenisation des corpus
"""

from collections import OrderedDict
from typing import Optional
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datastructures import Corpus


def get_accuracy(ecorpus: Corpus, rcorpus: Corpus, subcorpus: Optional[str]) -> tuple[float, float]:
    """
    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
        subcorpus (Optional[str]): nom du sous-corpus du corpus test à évaluer

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


def get_matrice(ecorpus: Corpus, rcorpus: Corpus, subcorpus: Optional[str]):
    """fonction d'affichage des matrices de confusion
    pour la classification des pos

    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
    """
    
    etags = {token.pos for sentence in ecorpus.sentences for token in sentence.tokens}
    rtags = {token.pos for sentence in rcorpus.sentences for token in sentence.tokens}
    tags = etags.union(rtags)

    # 'epos_rpos' est un dictionnaire (clé = epos) de dictionnaire (clé = rpos)
    epos_rpos = OrderedDict()
    for etag in tags: # tag du modèle à évaluer
        epos_rpos[etag] = OrderedDict()
        for rtag in tags: # tag du corpus de référence
            epos_rpos[etag][rtag] = 0

    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences):
        if subcorpus is None:
            for etoken, rtoken in zip(esentence.tokens, rsentence.tokens):   
                epos_rpos[etoken.pos][rtoken.pos] += 1    
        else:
            if rsentence.sent_id == subcorpus :
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


def test_tokens(ecorpus: Corpus, rcorpus: Corpus):
    """fonction d'affichage pour voir les résultats obtenus
        après l'obtention des corpus

    Args:
        ecorpus (Corpus): corpus à évaluer
        rcorpus (Corpus): corpus de référence
    """
    # pour voir sur le terminal la tokenisation des deux corpus
    print("etoken", "\t", "rtoken")
    for esentences, rsentences in zip(ecorpus.sentences, rcorpus.sentences):
        for etoken, rtoken in zip(esentences.tokens, rsentences.tokens):
            # plusieurs proposition aux choix en fonction de ce que l'on veut voir
            if etoken.pos != rtoken.pos:
                print(etoken, "\t", rtoken)
            # print(etoken, "\t", rtoken)
            # print(etoken.form, "\t", rtoken.form)
            # print(etoken.pos, "\t", rtoken.pos)
