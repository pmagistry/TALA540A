import spacy

## étape 2

"""
Essayer d'utiliser `typing` et des `dataclass` pour structurer votre code

- partir du texte brut
- imposer la tokenisation de sequoia
    - cf. https://spacy.io/usage/linguistic-features#own-annotations
    - ou cf. https://spacy.io/api/doc
    - Quelles différences ?
""" 

nlp = spacy.load("fr_core_web_sm")

doc = nlp("This is a sentence.")
print([(w.text, w.pos_) for w in doc])