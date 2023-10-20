#!/usr/bin/env python
# coding: utf-8

from datastructures import Corpus

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def get_tags(ecorpus: Corpus, rcorpus: Corpus) -> list :
    # certains tags ne sont présents que dans un des deux corpus 
    # on crée donc deux liste de tags pour la precision et le rappel
    etags = []
    for esentence in ecorpus.sentences :
        for token in esentence.tokens :
            if token.pos not in etags :
                etags.append(token.pos)
    rtags =[]
    for rsentence in rcorpus.sentences :
        for token in rsentence.tokens :
            if token.pos not in rtags :
                rtags.append(token.pos)

    return etags, rtags

def get_accuracy(ecorpus: Corpus, rcorpus: Corpus) -> float : 
    # nb de docs bien classés (vrai positif) / nb total de docs à classer
    
    total = 0
    total_oov = 0
    
    acc = 0 # sans tenir compte de is_oov
    acc_oov = 0
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences) :
        for etoken, rtoken in zip(esentence.tokens, rsentence.tokens) :
            assert(etoken.form == rtoken.form)

            total += 1 # sans vocab
            if etoken.pos == rtoken.pos :
                acc +=1

            if rtoken.is_oov : # avec vocab
                total_oov += 1
                if etoken.pos == rtoken.pos :
                    acc_oov +=1

    return round(acc / total * 100, 2), round(acc_oov / total_oov * 100, 2)

def get_precision(ecorpus: Corpus, rcorpus: Corpus, tag: str) -> float  : 
    # nb de docs correctement attribués à la classe i (vrai positif) / nb de docs attribués à la classe i (vrai positif et faux positif)
    all_positive = 0
    true_positive = 0
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences) :
        for etoken, rtoken in zip(esentence.tokens, rsentence.tokens) :
            if etoken.pos == tag :
                all_positive += 1
            if etoken.pos == rtoken.pos and etoken.pos == tag :
                true_positive +=1
    return round(true_positive / all_positive * 100, 2)

def get_rappel(ecorpus: Corpus, rcorpus: Corpus, tag: str) -> float  :
    # nb de docs correctement attribués à la classe i (vrai positif) / nb de docs appartenant à la classe i (vrai positif et faux negatif)
    all_positive = 0
    true_positive = 0
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences) :
        for etoken, rtoken in zip(esentence.tokens, rsentence.tokens) :
                if rtoken.pos == tag :
                    all_positive += 1
                if etoken.pos == rtoken.pos and etoken.pos == tag :
                    true_positive +=1
    return round(true_positive / all_positive * 100, 2)

def get_matrice(ecorpus: Corpus, rcorpus: Corpus) :
    
    # on crée d'abord un dictionnaire de dictionnaire
    epos_rpos = defaultdict(lambda: defaultdict(int))
    for esentence, rsentence in zip(ecorpus.sentences, rcorpus.sentences) :
        for etoken, rtoken in zip(esentence.tokens, rsentence.tokens) :
            epos_rpos[etoken.pos][rtoken.pos] += 1

    # on peut obtenir un matrice avec pandas
    cm = pd.DataFrame.from_dict(epos_rpos)
    # remplace les NaN par des 0 -> important pour les calculs après
    cm = cm.fillna(0)
    
    # on a une matrice de confusion basique
    print(cm) # colonne rpos, ligne epos
    
    # si l'on souhaite rajouter quelques couleurs
    f, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True)

    # titre du graphe et des axes
    plt.title("Matrice de confusion - données de test", fontsize=20, fontweight="bold")
    plt.xlabel("Etiquette prédite", fontsize=14)
    plt.ylabel("Etiquette correcte", fontsize=14)

    # affichage
    plt.show()