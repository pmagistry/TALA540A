'''
Étape 1 : 

Utilisation de l'envrionnement "myenv"
Ligne de commande : conda activate myenv 

Version texte brut : cat fr_sequoia-ud-test.conllu | grep "# text" | sed 's/# text = //'
> fichier : resultats.txt

'''


# 1ère version d'une tokenisation de sequoia 

'''
import spacy 

chemin_fichier = "resultats.txt"

with open(chemin_fichier, "r", encoding="utf-8") as file:
    texte = file.read()

nlp = spacy.load ("fr_core_news_sm")

def tokenize_text(texte):
    doc = nlp(texte)
    tokens = [token.text for token in doc]
    return tokens

print(tokenize_text(texte))

'''
'''
# 2. tokenisation de sequoia 
doc = nlp("resultats.txt")
from spacy.tokens import Doc 


words = ["hello", "world", "!"]
spaces = [True, False, False]
doc = Doc(nlp.vocab, words=words, spaces=spaces)

print(doc)
'''

# Correction 

from typing import List, Union, Dict 
from pathlib import Path 
from dataclasses import dataclass 

from spacy import Language
from spacy.tokens import Token as SpacyToken, Doc as SpacyDoc 
import spacy 

# Définition d'une classe "Token" avec deux attributs : "form" (forme du mot) et "tag" (étiquette grammaticale).
@dataclass
class Token():
    form : str 
    tag : str 

# Définition d'une classe "Sentence" qui contient une liste de tokens.
@dataclass
class Sentence():
    tokens: List[Token]

# Définition d'une classe "Corpus" qui contient une liste de phrases (sentences).
@dataclass
class Corpus():
    sentences: List[Sentence]

# Fonction pour lire un fichier au format CoNLL et retourner un objet "Corpus" contenant les données lues.
def read_conll(path: Path ) -> Corpus : 
    sentences = []  # Initialisation d'une liste vide pour stocker les phrases.
    with open(path) as f:  # Ouverture du fichier situé au chemin spécifié dans "path".
        tokens = []  # Initialisation d'une liste vide pour stocker les tokens de la phrase en cours.
        for line in f:  # Parcours de chaque ligne du fichier.
            line = line.strip()  # Suppression des espaces vides à la fin de la ligne.
            if not line.startswith('#'):  # Vérification que la ligne n'est pas un commentaire.

                if line == "": 
                    # Si la ligne est vide, cela signifie la fin d'une phrase.
                    # On crée un objet "Sentence" avec les tokens collectés jusqu'à présent et on l'ajoute à la liste "sentences".
                    sentences.append(Sentence(tokens))
                    tokens = []  # Réinitialisation de la liste "tokens" pour la phrase suivante.
                else : 
                    # Si la ligne contient un token, on la divise en champs et on extrait la forme du mot et l'étiquette grammaticale.
                    fields = line.split("\t")
                    form, tag = fields[1], fields[3]
                    if not tag == "_": 
                        # Si l'étiquette n'est pas "_", on crée un objet "Token" et on l'ajoute à la liste "tokens".
                        tokens.append(Token(form, tag))
    return Corpus(sentences)  # Retourne un objet "Corpus" contenant toutes les phrases extraites du fichier.

# Fonction pour étiqueter un corpus à l'aide d'un modèle Spacy.
def tag_corpus_spacy(corpus: Corpus, model_spacy: spacy.language) -> Corpus : 
    sentences = []
    for sentences in corpus : 
        doc = sentence_to_doc(Sentence, model_spacy)
        # doc = def append(object:_T, /) -> None 
        sentences.append(doc_to_sentence(doc))

    return Corpus (sentences) 

def sentence_to_doc(sentence : Sentence, vocab) -> SpacyDoc : 
    words = [tok.form for tok in sentence.tokens]
    return SpacyDoc(vocab, words=words)

def doc_to_sentence(doc: SpacyDoc) -> Sentence: 
    tokens = []
    for tok in doc : 
        tokens.append(Token(tok.text, tok.pos_))
    return Sentence(tokens)
    

# Fonction pour calculer l'exactitude (accuracy) entre un corpus "gold" et un corpus "test".
def compute_accuracy(corpus_gold: Corpus, corpus_test: Corpus) -> float: 
    nb_ok = 0  # Compteur pour les tokens correctement étiquetés.
    nb_total = 0  # Compteur pour le nombre total de tokens.
    for sentence_gold, sentence_test in zip(corpus_gold.sentences, corpus_test.sentences):
        for token_gold, token_test in zip(sentence_gold.tokens, sentence_test.tokens): 
            assert(token_gold.form == token_test.form )  # Vérification que les formes des tokens correspondent.
            if token_gold.tag == token_test.tag: 
                nb_ok += 1  # Incrémentation du compteur si l'étiquette est correcte.
            nb_total += 1  # Incrémentation du compteur total.
    return nb_ok / nb_total  # Calcul de l'exactitude en divisant les tokens corrects par le nombre total de tokens.

# Fonction principale qui lit un corpus "gold" à partir d'un fichier et l'affiche.
def main():
    modele_spacy = spacy.load("fr_core_news_sm")
    corpus_gold = read_conll("fr_sequoia-ud-test.conllu")
    corpus_test = tag_corpus_spacy(corpus_gold, modele_spacy)
    print(compute_accuracy(corpus_gold, corpus_test))

if __name__ == "__main__":
    main()  # Exécute la fonction principale
