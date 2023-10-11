#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: florianj

Description : script pour évaluer le pos tagging d'un outil NLP

Exécution : 
python3 script/evaluation_outil.py corpus.conllu

    Exemple :
python3 script/evaluation_outil.py DATA/fr_sequoia-ud-test.conllu

"""

import sys, spacy
from spacy.tokens import Doc
import corpus

# calcul de la précision : pourcentage d'élements correctement prédits par rapport au nombre total d'élément prédits
def precision(reference_list, predicted_list):
    correct_predicted = sum(1 for element in predicted_list if element in reference_list)
    total_predicted = len(predicted_list)
    accuracy = correct_predicted / total_predicted
    return accuracy

# calcul du rappel : pourcentage d'élément correctement prédits par rapport au nombre total d'élément de référence
def recall(reference_list, predicted_list):
    correct_predicted = sum(1 for element in predicted_list if element in reference_list)
    total_predicted = len(reference_list)
    recall = correct_predicted / total_predicted
    return recall

# calcul du f-score : combinaison des mesures de précision et rappel
def f_score(reference_list, predicted_list):
    precision_score = precision(reference_list, predicted_list)
    recall_score = recall(reference_list, predicted_list)
    # print(f"precision:{precision_score}")
    # print(f"rappel:{recall_score}")
    if (precision_score == 0 and recall_score == 0): # pour le cas d'une division par 0
        f = 0
    else:
        f = 2 * (precision_score * recall_score) / (precision_score + recall_score)
    # print(f"f-score:{f}")
    return f

# evaluation de la tokenisation de spacy
def spacy_tokenisation_evaluation(spacy_model, corpus):
    nlp = spacy.load(spacy_model)
    dict_acc = {}
    sum_acc = 0

    for sentence in corpus.sentences:
        list_token_ref = [token.form for token in sentence.tokens]
        
        doc = nlp(sentence.text)
        list_token_spacy = [token.text for token in doc]

        accuracy = precision(reference_list=list_token_ref, predicted_list=list_token_spacy)
        dict_acc.update({sentence.id: accuracy})
        sum_acc += accuracy
    acc_mean = sum_acc/len(corpus.sentences)
    print(f"L'accuracy moyenne du modèle {spacy_model} de spacy pour la tokenisation sur le corpus {corpus.type} est de : {round(acc_mean,2)}")

# evaluation du POS tagging de spacy
def spacy_pos_tagging_evaluation(spacy_model, corpus):
    nlp = spacy.load(spacy_model)
    dict_acc = {}
    sum_acc = 0

    for sentence in corpus.sentences:
        list_pos_ref = [token.upos for token in sentence.tokens]
        
        tokens = [token.form for token in sentence.tokens]
        doc = Doc(nlp.vocab, words=tokens)
        
        list_pos_spacy = [token.pos_ for token in nlp(doc)]
        
        # accuracy = precision(reference_list=list_pos_ref, predicted_list=list_pos_spacy)
        accuracy = f_score(reference_list=list_pos_ref, predicted_list=list_pos_spacy)
        dict_acc.update({sentence.id: accuracy})
        sum_acc += accuracy
    acc_mean = sum_acc/len(corpus.sentences)
    print(f"L'accuracy moyenne du modèle {spacy_model} de spacy pour le pos tagging sur le corpus {corpus.type} est de : {round(acc_mean,2)}")

if __name__ == "__main__":
    corpus = corpus.make_corpus(sys.argv[1])
    # spacy_model = "fr_core_news_sm"
    spacy_model = "ja_core_news_sm"

    # spacy_tokenisation_evaluation(spacy_model=spacy_model, corpus=corpus)
    spacy_pos_tagging_evaluation(spacy_model=spacy_model, corpus=corpus)
