#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datastructures import Token, Corpus, Phrase
import spacy

def recup_token():
    tokenisation = []

    with open("../corpus/fr_sequoia-ud-test.conllu", 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()

    en_cours = None #Stocker la phrase en cours
    tokens_phr = []

    for ligne in lignes:
        if not ligne.startswith("#"):
            if en_cours:
                en_cours.tokens = tokens_phr
                tokenisation.append(en_cours)

            # Créez une nouvelle phrase
            metadata = ligne.strip().split("= ")
            phr_id = int(metadata[0].split("sent_id = ")[1])
            texte = metadata[1]
            en_cours = Phrase(phr_id=phr_id, texte=texte, tokens=[])
            tokens_phr = []

        elif not ligne.startswith("#"):
            elements = ligne.split("\t")
            if len(elements) == 10:  # S'assurer q la ligne contient 10 éléments (format CoNLL-U standard)
                id = int(elements[0])
                forme = elements[1]
                lemme = elements[2]
                upos = elements[3]
                tokens_phr.append(Token(id=id, forme=forme, lemme=lemme, upos=upos))

    # Enregistrez la dernière phrase
    if en_cours:
        en_cours.tokens = tokens_phr
        tokenisation.append(en_cours)

    return tokenisation

def get_texte():
    with open("../corpus/textebrut.txt", 'r', encoding='utf-8') as fichier_brut:
        texte_brute = fichier_brut.read()

        doc = nlp(texte_brute)

        for token in doc:
            print(f"Token ID : {token.i}, Forme : {token.text}, Lemme : {token.lemma_}, UPOS : {token.pos_}")

