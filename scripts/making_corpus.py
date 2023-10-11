#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# Importation des classes
#
from datastructures import Token, Sentence, Corpus

def make_corpus(file_name):
    # Initialisation d'une instance de Corpus
    corpus = Corpus(sentences=[])

    with open(file_name, 'r', encoding='utf-8') as f:
        sentence_data = []
        sentence_text = ""  # Pour stocker le texte brut de la phrase
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                if sentence_data:
                    sentence = Sentence(tokens=sentence_data, text=sentence_text)
                    corpus.sentences.append(sentence)
                    sentence_data = []
                    sentence_text = ""
                continue
            parts = line.split('\t')
            if len(parts) == 10:
                # Vérifie si la valeur dans la colonne HEAD peut être convertie en entier
                try:
                    head_int = int(parts[6])
                except ValueError:
                    # Si la conversion échoue, ignore ce token
                    continue

                token = Token(int(parts[0]), parts[1], parts[2], parts[3], head_int, parts[7])
                sentence_data.append(token)
                sentence_text += parts[1] + " "  # Ajoute le mot au texte brut

    if sentence_data:
        sentence = Sentence(tokens=sentence_data, text=sentence_text)
        corpus.sentences.append(sentence)

    return corpus
