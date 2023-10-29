#!/usr/bin/env python
# coding: utf-8

"""
Ce fichier contient les fonctions pour obtenir les objets de la classe Corpus
    pour les fichiers conllu
"""

from typing import Set, Optional
import regex
from tqdm import tqdm
from conllu import parse, SentenceList
from datastructures import Token, Sentence, Corpus


def get_vocab(corpus_train: Corpus) -> Set[str]:
    """
    Args:
        corpus_train (Corpus): corpus train de la langue étudiée

    Returns:
        Set[str]: renvoie le vocabulaire du corpus train
    """
    return {
        token.form for sentence in corpus_train.sentences for token in sentence.tokens
    }


def sequoia_conllu(fichier) -> SentenceList:
    """
    Returns:
    Args:
        fichier (str): test ou train en fonction du fichier à parser

        SentenceList: liste des tables parsées
    """
    if fichier == "train":
        with open(
            "./corpus/fr_sequoia-ud-train.conllu", "r", encoding="utf-8"
        ) as file:
            data = file.read()
    else:
        with open("./corpus/fr_sequoia-ud-test.conllu", "r", encoding="utf-8") as file:
            data = file.read()
    return parse(data)


def gsd_conllu(fichier) -> SentenceList:
    """
    Args:
        fichier (str): test ou train en fonction du fichier à parser

    Returns:
        SentenceList: liste des tables parsées
    """
    if fichier == "train":
        with open(
            "./corpus/zh_gsdsimp-ud-train.conllu", "r", encoding="utf-8"
        ) as file:
            data = file.read()
    else:
        with open("./corpus/zh_gsdsimp-ud-test.conllu", "r", encoding="utf-8") as file:
            data = file.read()
    return parse(data)


def get_conllu(
    langue: str, fichier: str, vocabulaire: Optional[Set[str]] = None
) -> Corpus:
    """
    Args:
        langue (str): langue du corpus
        fichier (str): test ou train
        vocabulaire (Optional[Set[str]], optional): vocab du corpus train de référence

    Returns:
        Corpus: contient les informations du corpus test de référence
    """
    # 'tables' est une SentenceList, chaque élément correspond à un tableau dans le fichier conllu
    if langue == "zh":  # choix de la langue : chinois
        tables = gsd_conllu(fichier)
    else:  # choix de la langue par défaut : français
        tables = sequoia_conllu(fichier)

    # démarrage de l'instanciation de l'object Corpus et du compteur tqdm
    with tqdm(total=len(tables), colour="WHITE", desc="phrases conllu") as tqdmbar:
        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for table in tables:
            # 'sent_id' contient le nom du sous-corpus d'où vient la phrase
            sent_id = regex.search(r"^.+(\.|-)", table.metadata["sent_id"]).group(0)

            # 'tokens' est une liste d'objet de la classe Token
            tokens = []
            # on récupère les tokens dans chaque phrase (chaque table)
            for token in table:
                if not token["upos"] == "_":  # éviter les contractions type "du"
                    if vocabulaire is None:
                        is_oov = True
                    else:
                        is_oov = not token["form"] in vocabulaire
                    tokens.append(
                        Token(form=token["form"], pos=token["upos"], is_oov=is_oov)
                    )
            sentences.append(
                Sentence(nb_tokens=len(tokens), sent_id=sent_id, tokens=tokens)
            )
            tqdmbar.update(1)  # update du compteur

    return Corpus(nb_sentences=len(sentences), sentences=sentences)
