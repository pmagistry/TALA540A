#!/usr/bin/env python
# coding: utf-8

"""
Ce fichier contient les fonctions pour obtenir les objets de la classe Corpus
"""

from typing import Set, Optional
from tqdm import tqdm
from conllu import parse, SentenceList
import spacy
from spacy.tokens import Doc
from spacy import Language as SpacyPipeline
from datastructures import Token, Sentence, Corpus


def sequoia_conllu() -> SentenceList:
    """
    Returns:
        SentenceList: liste des tables parsées
    """
    with open(f"./corpus/fr_sequoia-ud-test.conllu", "r", encoding="utf-8") as file:
        data = file.read()
    return parse(data)


def pud_conllu() -> SentenceList:
    """
    Returns:
        SentenceList: liste des tables parsées
    """
    with open(f"./corpus/zh_pud-ud-test.conllu", "r", encoding="utf-8") as file:
        data = file.read()
    return parse(data)


def get_conllu(langue: str, vocabulaire: Optional[Set[str]] = None) -> Corpus:
    """
    Args:
        langue (str): langue du corpus
        vocabulaire (Optional[Set[str]], optional): vocab du corpus de ref

    Returns:
        Corpus: contient les informations du corpus de référence
    """
    # 'tables' est une SentenceList, chaque élément correspond à un tableau dans le fichier conllu
    if langue == "zh":  # choix de la langue : chinois
        tables = pud_conllu()
    else:  # choix de la langue par défaut : français
        tables = sequoia_conllu()

    # démarrage de l'instanciation de l'object Corpus et du compteur tqdm
    with tqdm(total=len(tables), colour="blue", desc="phrases conllu") as tqdmbar:
        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for table in tables:
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
            sentences.append(Sentence(nb_tokens=len(tokens), tokens=tokens))
            tqdmbar.update(1)  # update du compteur

    return Corpus(nb_sentences=len(sentences), sentences=sentences)


def get_model(langue: str) -> SpacyPipeline:
    """
    Args:
        langue (str): langue du corpus

    Returns:
        SpacyPipeline: modèle de spacy que l'on a entrainé
    """
    if langue == "zh":  # choix de la langue : chinois
        nlp = spacy.load("./script/model_zh/model-best")

    else:  # choix par défaut de la langue : français
        nlp = spacy.load("./script/model_fr/model-best")

    return nlp

def get_spacy_mymodel(langue: str, rcorpus: Corpus) -> Corpus:
    """
    Args:
        langue (str): langue du corpus
        rcorpus (Corpus): corpus de référence

    Returns:
        Corpus: contient les informations du corpus à évaluer
    """
    # 'nlp' est le modèle spacy que l'on a choisi en argument
    nlp = get_model(langue)

    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(
        total=rcorpus.nb_sentences, colour="magenta", desc="phrases spacy"
    ) as tqdmbar:
        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for rsentence in rcorpus.sentences:
            # 'words' est une liste de tokens
            # dont on a récupéré la forme dans le corpus de référence
            words = [tok.form for tok in rsentence.tokens]
            doc = Doc(nlp.vocab, words=words)
            doc = nlp(doc)
            # 'tokens' est une liste d'objet de la classe Token
            tokens = []
            for etoken, rtoken in zip(doc, rsentence.tokens):
                tokens.append(Token(etoken.text, etoken.pos_, is_oov=rtoken.is_oov))
            sentences.append(Sentence(nb_tokens=len(tokens), tokens=tokens))
            tqdmbar.update(1)  # update du compteur

    return Corpus(nb_sentences=rcorpus.nb_sentences, sentences=sentences)

def test_tokens(ecorpus: Corpus, rcorpus: Corpus):
    """ fonction d'affichage pour voir les résultats obtenus 
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
            # if etoken.pos != rtoken.pos:
            #     print(etoken, "\t", rtoken)
            print(etoken, "\t", rtoken)
            # print(etoken.form, "\t", rtoken.form)
            # print(etoken.pos, "\t", rtoken.pos)
