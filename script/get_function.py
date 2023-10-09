#!/usr/bin/env python
# coding: utf-8

import spacy
from spacy.tokens import Doc
from tqdm import tqdm
from conllu import parse
from datastructures import Token, Sentence, Corpus


def get_spacy() :
    with open(f'./corpus/textebrut.txt', "r") as f : # texte brut recupere a l'avance du fichier conllu
        data = f.readlines()

    nlp = spacy.load("fr_core_news_sm") # on load le modele
    list_sentences = []

    with tqdm(total=len(data), colour="red", desc="spacy") as bar: # sert pour la barre d'avancement, rajoute +1 à chaque phrase analysée
        
        for line in data :
            doc = nlp(line)

            list_analyses = [] # on cherche à obtenir une liste avec l'analyse de chaque token
            for token in doc:
                list_analyses.append(Token(form=token.text, lemma=token.lemma_, pos=token.pos_))

            list_sentences.append(Sentence(number_tokens=len(doc), analyses=list_analyses))
            
            bar.update(1) # update la barre
    
    return Corpus(number_lines=len(list_sentences), sentences=list_sentences) # renvoie une instance de la classe Corpus


def get_spacy_retokenize(sentences_conllu) :
    sentences = sentences_conllu # on va chercher la tokenisation du corpus

    nlp = spacy.blank("fr") # on a pas besoin d'un modele particulier car on utilise la tokenisation de sequoia
    list_sentences = []

    with tqdm(total=len(sentences), colour="magenta", desc="spacy_retokenize") as bar:
        
        for line in sentences :
            words = [token['form'] for token in line] # on récupère les infos dans le fichier conllu
            lemmas = [token['lemma'] for token in line]
            pos = [token['upos'] for token in line]
            pos = [word.replace('_','X') for word in pos] # spacy bloque si un pos ne fait pas partie de la liste UD
 
            doc = Doc(nlp.vocab, words=words, lemmas=lemmas, pos=pos) # on parse le texte avec nos informations   

            list_analyses = [] # on cherche à obtenir une liste avec l'analyse de chaque token
            for token in doc:
                list_analyses.append(Token(form=token, lemma=token.lemma_, pos=token.pos_))

            list_sentences.append(Sentence(number_tokens=len(doc), analyses=list_analyses))
            
            bar.update(1) # update du compteur
    
    return Corpus(number_lines=len(list_sentences), sentences=list_sentences) # renvoie une instance de la classe Corpus


def get_conllu() :
    with open(f'./corpus/fr_sequoia-ud-test.conllu', "r") as f :
        data = f.read()
    sentences = parse(data)

    with tqdm(total=len(sentences), colour="blue", desc="conllu") as bar:
        list_sentences = []
        for sentence in sentences :
            list_analyses = []
            for token in sentence :
                list_analyses.append(Token(form=token['form'], lemma=token['lemma'], pos=token['upos'].replace('_', 'X'))) 
                # on remplace les _ par X car le signe _ ne fait pas partie des pos de UD
            list_sentences.append(Sentence(number_tokens=[token['id'] for token in sentence][-1], analyses=list_analyses))
            bar.update(1)

    return sentences, Corpus(number_lines=len(list_sentences), sentences=list_sentences) # renvoie une instance de la classe Corpus et le fichier conllu parse


def get_pos(corpus) :
    list_sentences_pos = []
    list_pos = []
    for sentences in corpus.sentences :
        pos = []
        for token in sentences.analyses :
            pos.append(token.pos)
            list_pos.append(token.pos)
        list_sentences_pos.append(pos)
    return list_sentences_pos, list_pos # liste de liste de pos


def get_accuracy(lrpos, lepos, epos) :  # nb de documents bien classés (vrai positif) / nb total de documents à classer (tout le corpus)
    acc = 0
    for n in range(len(lepos)) :  # compteur pour la liste de phrase où chaque phrase est une liste de tous les pos de la phrase
        
        if len(lepos[n]) > len(lrpos[n]) : # pour eviter l'erreur de index out of range
            m_compteur = len(lrpos[n])
        else :
            m_compteur = len(lepos[n])
            
        for m in range(m_compteur) : # compteur pour la liste de pos
            if lepos[n][m] == lrpos[n][m] :
                acc +=1

    return acc / len(epos)


def get_precision(lrpos, lepos, epos, upos) : # nb de documents correctement attribués à la classe i (vrai positif) / nb de docs attribués à la classe i (vrai positif et faux positif)
    pre = 0
    for n in range(len(lepos)) :  # compteur pour la liste de phrase où chaque phrase est une liste de tous les pos de la phrase
        
        if len(lepos[n]) > len(lrpos[n]) : # pour eviter l'erreur de index out of range
            m_compteur = len(lrpos[n])
        else :
            m_compteur = len(lepos[n])
            
        for m in range(m_compteur) : # compteur pour la liste de pos
            if lepos[n][m] == lrpos[n][m] and lepos[n][m] == upos :
                pre +=1

    return pre / len([pos for pos in epos if pos == upos])


def get_rappel(lrpos, lepos, rpos, upos) : # nb de documents correctement attribués à la classe i (vrai positif) / nb de docs appartenant à la classe i (vrai positif et faux negatif)
    rap = 0
    for n in range(len(lepos)) :  # compteur pour la liste de phrase où chaque phrase est une liste de tous les pos de la phrase
        
        if len(lepos[n]) > len(lrpos[n]) : # pour eviter l'erreur de index out of range
            m_compteur = len(lrpos[n])
        else :
            m_compteur = len(lepos[n])
            
        for m in range(m_compteur) : # compteur pour la liste de pos
            if lepos[n][m] == lrpos[n][m] and lepos[n][m] == upos :
                rap +=1
    
    return rap / len([pos for pos in rpos if pos == upos])