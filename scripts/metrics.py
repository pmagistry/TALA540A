#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# Modules
#
import timeit
from sklearn.metrics import confusion_matrix

# Mesure l'exactitude en comparant les POS prédits avec les POS réels
def measure_accuracy(processed_docs):
    correct_tags = 0
    total_tags = 0
    correct_oov_tags = 0
    total_oov_tags = 0

    # Parcoure chaque document dans le corpus
    for doc in processed_docs:
        for token in doc:
            # Compare le pos prédit (pos_) avec le pos réel (tag_)
            if token.pos_ == token.tag_:
                correct_tags += 1
                if token.is_oov:
                    correct_oov_tags += 1
            total_tags += 1
            if token.is_oov:
                total_oov_tags += 1

    # Calcul l'exactitude (en pourcentage)
    accuracy = (correct_tags / total_tags) * 100
    oov_accuracy = (correct_oov_tags / total_oov_tags) * 100
    return accuracy, oov_accuracy

# Mesure le temps d'exécution de l'analyse de texte avec un modèle spacy
def measure_execution_time(model, text):
    # Prépare le code pour charger le modèle Spacy et analyser le texte
    setup_code = f"import spacy; nlp = spacy.load('{model}')"
    stmt = f"nlp('{text}')"
    # Mesure le temps d'exécution de l'analyse pour 1000 itérations
    execution_time = timeit.timeit(stmt, setup=setup_code, number=1000)
    return execution_time

# Génère une matrice de confusion à partir des POS réels et prédits
def generate_confusion_matrix(processed_docs):
    true_tags = []
    predicted_tags = []

    # Collecte des POS réels et prédits pour chaque token
    for doc in processed_docs:
        for token in doc:
            true_tags.append(token.tag_)  # POS réels
            predicted_tags.append(token.pos_)  # POS prédits

    # Crée la liste des labels en utilisant l'ensemble des POS réels et prédits
    labels = list(set(true_tags + predicted_tags))
    # Génère la matrice de confusion
    confusion = confusion_matrix(true_tags, predicted_tags, labels=labels)
    return confusion