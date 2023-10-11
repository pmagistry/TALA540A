#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:21:56 2023

@author: orane
"""

import re
import pyconll
import typing 
import spacy
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
    
def load_text(file) -> str :
    with open(file, "r") as f:
        text = f.read()
        clean_text = re.sub("\n", " ", text)
    return clean_text

text = load_text("fr_sequoia.txt")

def tokenize_and_anotate(text: str) -> list :
    tokoov = []
    tokpos = []
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(text)
    for token in doc :
        tokpos.append((token.text,token.pos_))
        if token.is_oov :
            tokoov.append(token.text)
    return tokpos, tokoov

tokpos_spacy, _spacy = tokenize_and_anotate(text)

def extract_conll(file) -> list :
    tokpos = []
    f = pyconll.load_from_file(file)
    for sentence in f :
        i = 0
        while i < len(sentence):
            if sentence[i].form == "" or sentence[i].form == "\n":
                i += 1
            if "-" in sentence[i].id :
                tokpos.append((sentence[i].form, sentence[i+1].upos))
                i+= len(sentence[i].id.split("-")) +1
            else :
                tokpos.append((sentence[i].form, sentence[i].upos))
                i += 1
    return tokpos
    
tokpos_gold = extract_conll("fr_sequoia-ud-test.conllu")

def collect_eval(tokpos_spacy, tokpos_gold) :
    VP = defaultdict(int)
    FP = defaultdict(lambda: defaultdict(int))
    VN = defaultdict(int)
    FN = defaultdict(int)
    i_gold = 0
    i_spacy = 0
    while i_gold < len(tokpos_gold) and i_spacy < len(tokpos_spacy):
        if tokpos_spacy[i_spacy][0] == tokpos_gold[i_gold][0] :
            if tokpos_spacy[i_spacy][1] == tokpos_gold[i_gold][1] :
                VP[tokpos_spacy[i_spacy][1]] += 1
            else : 
                real_tag = tokpos_gold[i_gold][1]
                pred_tag = tokpos_spacy[i_spacy][1]
                FP[real_tag][pred_tag] += 1
                FN[real_tag] += 1        
        if len(tokpos_gold[i_gold][0]) <  len(tokpos_spacy[i_spacy][0]) : 
            real_tag = tokpos_gold[i_gold][1]
            pred_tag = tokpos_spacy[i_spacy][1]
            if real_tag != pred_tag : 
              FP[real_tag][pred_tag] += 1
            composed_word = tokpos_gold[i_gold][0]             
            while composed_word != tokpos_spacy[i_spacy][0] : 
                sep = ""
                for char in tokpos_spacy[i_spacy][0] :
                    if char == "h" :
                        sep = char
                    if not char.isalpha() and not char.isnumeric() :
                        sep = char     
                i_gold += 1
                nextword = tokpos_gold[i_gold][0]
                if sep == "'" or sep == "-" or sep == "°" or sep == "." or sep == "(" or sep == "\"" or sep == ")" or sep == "h":
                    composed_word += nextword 
                else : 
                    composed_word += sep + nextword           
        elif len(tokpos_spacy[i_spacy][0])  < len(tokpos_gold[i_gold][0]) :
            real_tag = tokpos_gold[i_gold][1]
            pred_tag = tokpos_spacy[i_spacy][1]
            if real_tag != pred_tag :
              FP[real_tag][pred_tag] += 1 
            composed_word = tokpos_spacy[i_spacy][0]  
            while composed_word != tokpos_gold[i_gold][0] :       
                sep = ""
                for char in tokpos_gold[i_gold][0] :
                    if char == "°":
                        sep = char
                        break
                    if not char.isalpha() and not char.isnumeric() :
                        sep = char
                i_spacy += 1
                nextword = tokpos_spacy[i_spacy][0]
                if sep == "'" or sep == "-"  or sep == "/" :
                    composed_word += nextword
                else : 
                    composed_word += sep + nextword
                
        i_gold += 1
        i_spacy += 1
        
    return dict(VP), dict(FP), dict(FN)
    


def generate_confusion_matrix(VP, FP, FN):
    all_tags = list(set(VP.keys()).union(FP.keys()).union(FN.keys()))
    confusion_matrix = pd.DataFrame(0, index=all_tags, columns=all_tags, dtype=int)


    for tag, count in VP.items():
        confusion_matrix.at[tag, tag] = count

    for real_tag, pred_tags in FP.items():
        for pred_tag, count in pred_tags.items():
            confusion_matrix.at[real_tag, pred_tag] = count

    return confusion_matrix

VP, FP, FN = collect_eval(tokpos_spacy, tokpos_gold)
confusion_data = generate_confusion_matrix(VP, FP, FN)

plt.figure(figsize=(12, 8))
sns.heatmap(confusion_data, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Real")
plt.title("Matrice de confusion")
plt.show()

def pos_metrics(VP, FP, FN):
    metrics = defaultdict(dict)
    all_tags = set(VP.keys()).union(FP.keys()).union(FN.keys())
    total = sum(VP.values()) + sum(sum(FP[tag].values()) for tag in FP) + sum(FN.values())
    for tag in all_tags:
        vp = VP[tag] if tag in VP else 0
        fp = sum(FP[tag].values()) if tag in FP else 0
        fn = FN[tag] if tag in FN else 0
        vn = total - vp - fp - fn

        recall = vp / (vp + fn) if (vp + fn) > 0 else 0
        precision = vp / (vp + fp) if (vp + fp) > 0 else 0
        accuracy = (vp + vn) / total if total > 0 else 0

        metrics[tag]["recall"] = recall
        metrics[tag]["precision"] = precision
        metrics[tag]["accuracy"] = accuracy

    return metrics
metrics = pos_metrics(VP, FP, FN)
print("---------------------------")
for key, value in metrics.items() :
    print(key, value)
print("---------------------------")

def overall_metrics(VP, FP, FN):
    total_vp = sum(VP.values())
    total_fp = sum(sum(FP[tag].values()) for tag in FP)
    total_fn = sum(FN.values())
    accuracy = total_vp / (total_vp + total_fp + total_fn)
    precision = total_vp / (total_vp + total_fp)
    recall = total_vp / (total_fn + total_vp)
    
    return accuracy, precision, recall

acc, precision, recall = overall_metrics(VP, FP, FN)
print("---------------------------")
print("accuracy : ", acc)
print("precision : ", precision)
print("recall : ", recall)
print("---------------------------")
