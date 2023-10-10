import spacy
from typing import List
from datastructure import Token # Importer la classe token depuis le fichier datastructure.py

# Charger le modéle Spacy pour le français
nlp = spacy.load("fr_core_news_md")

def load_file(filepath: str) -> str:
    """
    Charger le contenu du fichier 
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
    return data

def split_into_sentences(data: str) -> List[str]:
    """
    Diviser le texte en phrases avec Spacy
    """
    doc = nlp(data)
    return [sentence.text for sentence in doc.sents]

def extract_features(token):
    """
    Extraire les informations de features personnalisées pour un token.
    """
    features = []
#    if token.tag_:
#        features.append(token.tag_)
    if token.morph:
        for key, value in token.morph.to_dict().items():
            features.append(f"{key}={value}")
    return "|".join(features)

def tokenize_sentences(sentence: str) -> List[Token]:
    """
    Tokenisation des phrases et retourner une liste de tokens
    """
    doc = nlp(sentence)
    tokens_list = []
    for token in doc:
        features = extract_features(token)
        tokens = Token(
        token_id=token.i + 1,
        text=token.text,
        lemma=token.lemma_,
        pos=token.pos_,
        dep=token.dep_,
        features=features,
        head_id=token.head.i + 1 if token.head != token else 0,
        )
            
        tokens_list.append(tokens)
    return tokens_list


def main():
    # Chemin du fichier à traiter
    filepath = "fr_sequoia-ud-test.txt"

    # Charger le fichier
    data = load_file(filepath)
    sentences = split_into_sentences(data)

    # Traiter chaque phrase et obtenir les informations des tokens
    for i, sentence in enumerate(sentences, start=1):
        token_list = tokenize_sentences(sentence)
        for token_info in token_list:
            print(f"{token_info.token_id}\t{token_info.text}\t{token_info.lemma}\t{token_info.pos}\t{token_info.features}\t_\t_\t{token_info.head_id}\t{token_info.dep}\t_")
    
    
if __name__ == "__main__":
    main()