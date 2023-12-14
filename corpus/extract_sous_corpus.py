#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    python corpus/extract_sous_corpus.py

Ce fichier va extraire un ou plusieurs sous-corpus pour ensuite entrainer notre tokeniseur dessus
"""

# adding get_corpus and datastructures to the system path
import sys
sys.path.insert(0, 'evaluations/')

from get_corpus import get_conllu

def main():
    
    # on parse le fichier conllu et on crée une instance de la classe corpus
    corpus = get_conllu("dev")
    
    # on ne prend les phrases que si elle font partie du sous-corpus que l'on a choisi
    sentences = [ sentence for sentence in corpus.sentences if "KR1h0004" in sentence.sent_id ]
    
    # on print la phrase au format conllu
    for sentence in sentences:
        
        # 'resultats' est une string qui contient la phrase et ses informations au format conllu
        resultat = f"# sent_id = {sentence.sent_id}\n"
        texte = " ".join([token.form for token in sentence.tokens])
        resultat += f"# text = {texte}\n"
        
        # on crée la ligne du tableau de chaque token
        for i, token in enumerate(sentence.tokens):
            resultat += "\t".join([str(i+1), token.form, token.form, token.pos, token.pos, "_", "_", "_", "_", "_"]) + "\n"
        
        # on print le résultat soit sur le terminal soit dans un fichier
        print(resultat)

if __name__ == "__main__":
    main()
