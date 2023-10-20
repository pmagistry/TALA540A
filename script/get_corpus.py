#!/usr/bin/env python
# coding: utf-8


from tqdm import tqdm
from conllu import parse, SentenceList
from typing import Set, Optional
from datastructures import Token, Sentence, Corpus
import spacy
from spacy.tokens import Doc
from spacy import Language as SpacyPipeline

def sequoia_conllu() -> SentenceList :
    with open(f'./corpus/fr_sequoia-ud-test.conllu', "r") as f :
        data = f.read()
    return parse(data)

def pud_conllu() -> SentenceList :
    with open(f'./corpus/zh_pud-ud-test.conllu', "r") as f :
        data = f.read()
    return parse(data)

def get_conllu(langue: str, vocabulaire: Optional[Set[str]] = None) -> Corpus :
    
    if langue == "zh" : # choix de la langue : chinois
        tables = pud_conllu()
    else : # choix de la langue par défaut : français
        tables = sequoia_conllu()
        
    # démarrage de l'instanciation de l'object Corpus et du compteur tqdm
    with tqdm(total=len(tables), colour="blue", desc="phrases conllu") as bar:
        sentences = [] # liste d'objet de la classe Sentence
        for table in tables :
            tokens = [] # liste d'objet de la classe Token
            # on récupère les tokens dans chaque phrase (chaque table)
            for token in table :
                if not token["upos"] == "_" : # éviter les contractions type "du"
                    if vocabulaire is None:
                        is_oov = True
                    else:
                        is_oov = not token['form'] in vocabulaire
                    tokens.append(Token(form=token['form'], pos=token['upos'], is_oov=is_oov))
            sentences.append(Sentence(nb_tokens=len(tokens), tokens=tokens))
            bar.update(1) # update du compteur
            
    return Corpus(nb_sentences=len(sentences), sentences=sentences)

def get_model(langue: str, model: str) -> SpacyPipeline :
    
    if langue == "zh" : # choix de la langue : chinois
        if model == "trf" : # choix entre pls modèles de langue
            return spacy.load("zh_core_web_trf")
        elif model == "lg" :
            return spacy.load("zh_core_web_lg")
        elif model == "md" :
            return spacy.load("zh_core_web_md")
        else : # modèle par défaut
            return spacy.load("zh_core_web_sm")

    else : # choix par défaut de la langue : français
        if model == "trf" : # choix entre pls modèles de langue
            return spacy.load("fr_core_news_trf")
        elif model == "lg" :
            return spacy.load("fr_core_news_lg")
        elif model == "md" :
            return spacy.load("fr_core_news_md")
        else : # modèle par défaut
            return spacy.load("fr_core_news_sm")

def get_spacy_retok(langue: str, model: str, rcorpus: Corpus) -> Corpus :

    # d'abord, on récupère le modèle
    nlp = get_model(langue, model)
    
    # démarrage de l'instanciation de l'objet Corpus et du compteur tqdm
    with tqdm(total=rcorpus.nb_sentences, colour="magenta", desc="phrases spacy") as bar : 
        
        sentences = [] # liste d'objets de la classe Sentence
        for rsentence in rcorpus.sentences : 
            # on récupère les tokens dans le corpus de référence
            words = [tok.form for tok in rsentence.tokens] # on récupère leur forme
            doc = Doc(nlp.vocab, words=words)
            doc = nlp(doc)

            tokens= [] # liste d'objet de la classe Token
            for etoken, rtoken in zip(doc, rsentence.tokens) :
                tokens.append(Token(etoken.text, etoken.pos_, is_oov=rtoken.is_oov)) 
            
            sentences.append(Sentence(nb_tokens=len(tokens), tokens=tokens))        
            bar.update(1) # update du compteur

    return Corpus(nb_sentences=rcorpus.nb_sentences, sentences=sentences)

def test_tokens(ecorpus: Corpus, rcorpus: Corpus) :
    print("etoken", "\t", "rtoken")
    for esentences, rsentences in zip(ecorpus.sentences, rcorpus.sentences) :
        for etoken, rtoken in zip(esentences.tokens, rsentences.tokens) :
            if etoken.pos != rtoken.pos :
                print(etoken, "\t", rtoken)
            # print(etoken, "\t", rtoken)
            # print(etoken.form, "\t", rtoken.form)
            # print(etoken.pos, "\t", rtoken.pos)
            