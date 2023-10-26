#!/usr/bin/env python
# coding: utf-8

"""
Ce fichier contient les fonctions pour obtenir les objets de la classe Corpus
    pour les modèles spacy
"""

from tqdm import tqdm
import spacy
from spacy.tokens import Doc
from spacy import Language as SpacyPipeline
from datastructures import Token, Sentence, Corpus


def get_model(langue: str) -> SpacyPipeline:
    """
    Args:
        langue (str): langue du corpus

    Returns:
        list[str]: modèles de spacy choisi pour la tokenisation
    """
    if langue == "zh":  # choix de la langue : chinois
        models = ["zh_core_web_lg", "zh_core_web_md", "zh_core_web_sm"]

    else:  # choix par défaut de la langue : français
        models = ["fr_core_news_lg", "fr_core_news_md", "fr_core_news_sm"]
    
    return models


def get_spacy(langue: str, rcorpus: Corpus):
    """
    Args:
        langue (str): langue du corpus
        rcorpus (Corpus): corpus de référence

    Returns:
        Tuple(Corpus): contient les informations des trois corpus spacy
    """
    # 'models' est liste des noms des modèles spacy
    models = get_model(langue)
    
    # model lg
    nlp = spacy.load(models[0])

    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(
        total=rcorpus.nb_sentences, colour="magenta", desc="phrases spacy lg"
    ) as tqdmbar:
        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for rsentence in rcorpus.sentences:
            # 'words' est une liste de tokens
            # dont on a récupéré la forme dans le corpus de référence
            words = [tok.form for tok in rsentence.tokens]
            doc = Doc(nlp.vocab, words=words)
            doc = nlp(doc)
            
            # 'sent_id' contient le nom du sous-corpus d'où vient la phrase
            sent_id = rsentence.sent_id
            # 'tokens' est une liste d'objet de la classe Token
            tokens = []
            for etoken, rtoken in zip(doc, rsentence.tokens):
                tokens.append(Token(etoken.text, etoken.pos_, is_oov=rtoken.is_oov))
            sentences.append(Sentence(nb_tokens=len(tokens), sent_id=sent_id, tokens=tokens))
            tqdmbar.update(1)  # update du compteur
    
    corpus_lg = Corpus(nb_sentences=rcorpus.nb_sentences, sentences=sentences)
    
    # model md
    nlp = spacy.load(models[1])

    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(
        total=rcorpus.nb_sentences, colour="green", desc="phrases spacy md"
    ) as tqdmbar:
        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for rsentence in rcorpus.sentences:
            # 'words' est une liste de tokens
            # dont on a récupéré la forme dans le corpus de référence
            words = [tok.form for tok in rsentence.tokens]
            doc = Doc(nlp.vocab, words=words)
            doc = nlp(doc)
            
            # 'sent_id' contient le nom du sous-corpus d'où vient la phrase
            sent_id = rsentence.sent_id
            # 'tokens' est une liste d'objet de la classe Token
            tokens = []
            for etoken, rtoken in zip(doc, rsentence.tokens):
                tokens.append(Token(etoken.text, etoken.pos_, is_oov=rtoken.is_oov))
            sentences.append(Sentence(nb_tokens=len(tokens), sent_id=sent_id, tokens=tokens))
            tqdmbar.update(1)  # update du compteur
    
    corpus_md = Corpus(nb_sentences=rcorpus.nb_sentences, sentences=sentences)
    
    # model sm
    nlp = spacy.load(models[2])

    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(
        total=rcorpus.nb_sentences, colour="white", desc="phrases spacy sm"
    ) as tqdmbar:
        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for rsentence in rcorpus.sentences:
            # 'words' est une liste de tokens
            # dont on a récupéré la forme dans le corpus de référence
            words = [tok.form for tok in rsentence.tokens]
            doc = Doc(nlp.vocab, words=words)
            doc = nlp(doc)
            
            # 'sent_id' contient le nom du sous-corpus d'où vient la phrase
            sent_id = rsentence.sent_id
            # 'tokens' est une liste d'objet de la classe Token
            tokens = []
            for etoken, rtoken in zip(doc, rsentence.tokens):
                tokens.append(Token(etoken.text, etoken.pos_, is_oov=rtoken.is_oov))
            sentences.append(Sentence(nb_tokens=len(tokens), sent_id=sent_id, tokens=tokens))
            tqdmbar.update(1)  # update du compteur
    
    corpus_sm = Corpus(nb_sentences=rcorpus.nb_sentences, sentences=sentences)

    return corpus_lg, corpus_md, corpus_sm


def get_mymodel(langue: str) -> SpacyPipeline:
    """
    Args:
        langue (str): langue du corpus

    Returns:
        SpacyPipeline: modèle de spacy que l'on a entrainé
    """
    if langue == "zh":  # choix de la langue : chinois
        nlp = spacy.load("./script/model_spacy/model_zh/model-best")

    else:  # choix par défaut de la langue : français
        nlp = spacy.load("./script/model_spacy/model_fr/model-best")

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
    nlp = get_mymodel(langue)

    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(
        total=rcorpus.nb_sentences, colour="red", desc="phrases spacy"
    ) as tqdmbar:
        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for rsentence in rcorpus.sentences:
            # 'words' est une liste de tokens
            # dont on a récupéré la forme dans le corpus de référence
            words = [tok.form for tok in rsentence.tokens]
            doc = Doc(nlp.vocab, words=words)
            doc = nlp(doc)
            
            # 'sent_id' contient le nom du sous-corpus d'où vient la phrase
            sent_id = rsentence.sent_id
            # 'tokens' est une liste d'objet de la classe Token
            tokens = []
            for etoken, rtoken in zip(doc, rsentence.tokens):
                tokens.append(Token(etoken.text, etoken.tag_, is_oov=rtoken.is_oov))
            sentences.append(Sentence(nb_tokens=len(tokens), sent_id=sent_id, tokens=tokens))
            tqdmbar.update(1)  # update du compteur

    return Corpus(nb_sentences=rcorpus.nb_sentences, sentences=sentences)