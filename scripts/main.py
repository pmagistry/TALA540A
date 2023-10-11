#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# Modules
#
import spacy
from making_corpus import make_corpus
from metrics import measure_accuracy, measure_execution_time, generate_confusion_matrix

"""
Il suffit de lancer ce script pour obtenir le résultat de manière très simple : python main.py
Tous les modules nécessaires / fonctions des autres scripts sont appelés 
"""

# Charge le modèle spacy
nlp = spacy.load("fr_core_news_sm") 

# Chemin vers notre fichier conllu
conllu_file_path = '../data/fr_sequoia-ud-test.conllu'

# Charge les données du fichier conllu et crée un objet Corpus
corpus = make_corpus(conllu_file_path)

# Chemin vers notre fichier texte brut correspondant
text_file_path = '../data/texte_brut.txt'

# Lit le contenu du fichier texte brut
with open(text_file_path, 'r', encoding='utf-8') as f:
    raw_sentences = f.readlines()

# Traite chaque phrase brute avec spaCy
processed_docs = [nlp(sentence.strip()) for sentence in raw_sentences]

# Mesure l'exactitude en comparant les POS prédits avec les POS réels
accuracy, oov_accuracy = measure_accuracy(processed_docs)
print(f"Accuracy: {accuracy:.2f}%")
print(f"OOV Accuracy: {oov_accuracy:.2f}%")

# Mesure la vitesse (temps d'exécution de Spacy)
text_to_analyze = 'Votre texte à analyser ici'
execution_time = measure_execution_time("fr_core_news_sm", text_to_analyze)
print(f"Temps d'exécution moyen pour 1000 itérations : {execution_time:.2f} secondes")

# Génère la matrice de confusion en comparant les POS réels et prédits
confusion_matrix = generate_confusion_matrix(processed_docs)
print("Matrice de confusion :")
print(confusion_matrix)
