#!/usr/bin/env python
# coding: utf-8

"""
Ce fichier contient les fonctions pour obtenir les objets de la classe Corpus
    pour les fichiers conllu et less modèles spacy
"""

from typing import Set, Optional
import regex
from tqdm import tqdm
from conllu import parse
import spacy
from spacy.tokens import Doc
from jiayan import CRFPOSTagger
from datastructures import Token, Sentence, Corpus


def get_conllu(fichier: str, vocabulaire: Optional[Set[str]] = None) -> Corpus:
    """
    Args:
        fichier (str): test ou train
        vocabulaire (Optional[Set[str]], optional): vocab du corpus train de référence
    
    Returns:
        Corpus: contient les informations du corpus test de référence
    """
    
    # 'tables' est une SentenceList, chaque élément correspond à un tableau dans le fichier conllu
    if fichier == "train" :
        with open("./corpus/lzh_kyoto-ud-train.conllu", "r", encoding="utf-8") as f :
            data = f.read()
        tables = parse(data)
    elif fichier == "dev" :
        with open("./corpus/lzh_kyoto-ud-dev.conllu", "r", encoding="utf-8") as f :
            data = f.read()
        tables = parse(data)
    else : 
        with open("./corpus/lzh_kyoto-ud-test.conllu", "r", encoding="utf-8") as f :
            data = f.read()
        tables = parse(data)

    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(total=len(tables), colour="WHITE", desc=f"phrases conllu {fichier}") as tqdmbar:
        
        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for table in tables:
            
            # 'sent_id' contient le nom du sous-corpus d'où vient la phrase
            sent_id = regex.search(r"^[a-zA-Z0-9]+_", table.metadata["sent_id"]).group(0)

            # 'tokens' est une liste d'objet de la classe Token
            tokens = []
            # on récupère les tokens dans chaque phrase (chaque table)
            for token in table:
                if vocabulaire is None:
                    is_oov = True
                else:
                    is_oov = not token["form"] in vocabulaire
                tokens.append(Token(form=token["form"], pos=token["upos"], is_oov=is_oov))
            
            sentences.append(Sentence(nb_tokens=len(tokens), sent_id=sent_id, tokens=tokens))
            tqdmbar.update(1)  # update du compteur

    return Corpus(nb_sentences=len(sentences), sentences=sentences, name="conllu")


def get_spacy(rcorpus: Corpus, title: str, model: str, color: str) -> Corpus:
    """
    Args:
        rcorpus (Corpus): corpus de référence
        title (str): nom du titre du modèle spacy à afficher sur la barre tqdm
        model (str): nom du modèle spacy
        color (str): couleur de la barre tqdm (ne sert à rien mais ça fait jolie...)

    Returns:
        Corpus: contient les informations du corpus à évaluer
    """

    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(total=rcorpus.nb_sentences, colour=f"{color}", desc=f"{title}") as tqdmbar:
        
        # on récupère le modèle spacy
        nlp = spacy.load(model)
        
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
                # .tag_ s'il s'agit du modèle que l'on a entrainé
                if regex.match(r"corpus_[0-9]+", title):
                    tokens.append(Token(etoken.text, etoken.tag_, is_oov=rtoken.is_oov))
                # sinon .pos_
                else :
                    tokens.append(Token(etoken.text, etoken.pos_, is_oov=rtoken.is_oov))
            
            sentences.append(Sentence(nb_tokens=len(tokens), sent_id=sent_id, tokens=tokens))
            tqdmbar.update(1)  # update du compteur

    return Corpus(nb_sentences=rcorpus.nb_sentences, sentences=sentences, name=title)


def get_jiayan(rcorpus: Corpus, title: str, model: str, color: str):
    """
    Args:
        rcorpus (Corpus): corpus de référence
        title (str): nom du titre du modèle jiayan à afficher sur la barre tqdm
        model (str): nom du modèle jiayan
        color (str): couleur de la barre tqdm (ne sert à rien mais ça fait jolie...)

    Returns:
        Corpus: contient les informations du corpus à évaluer
    """

    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(total=rcorpus.nb_sentences, colour=f"{color}", desc=f"{title}") as tqdmbar:

        # on récupère le modèle 
        postagger = CRFPOSTagger()
        postagger.load(model)

        # 'sentences' est une liste d'objets de la classe Sentence
        sentences = []
        for rsentence in rcorpus.sentences:

            # 'words' est une liste de tokens
            # dont on a récupéré la forme dans le corpus de référence
            # 'words
            words = [tok.form for tok in rsentence.tokens]
            tags = postagger.postag(words)

            # 'sent_id' contient le nom du sous-corpus d'où vient la phrase
            sent_id = rsentence.sent_id

            # 'tokens' est une liste d'objet de la classe Token
            tokens = []
            for tag, rtoken in zip(tags, rsentence.tokens):
                tokens.append(Token(rtoken.form, tag, is_oov=rtoken.is_oov))
            
            sentences.append(Sentence(nb_tokens=len(tokens), sent_id=sent_id, tokens=tokens))
            tqdmbar.update(1)  # update du compteur

    return Corpus(nb_sentences=rcorpus.nb_sentences, sentences=sentences, name=title)