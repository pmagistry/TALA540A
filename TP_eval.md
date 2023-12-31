# TP Spacy POS tagging
Utilisation et évaluation de modèles pré-entraînés
(séances 1 et 2)

## Étape 1
### récupérer modèle et données

- création d'un venv si besoin
    - `python -m venv [nom_du_dossier]`
    - `source [nom_du_dossier]`
- `pip install spacy`
- `python -m spacy download fr_core_news_sm`
- trouver du corpus:
    - `wget https://github.com/UniversalDependencies/UD_French-Sequoia/raw/master/fr_sequoia-ud-test.conllu`
    - version texte brute: 
        `cat fr_sequoia-ud-test.conllu | grep "# text" | sed 's/# text = //'`
        

## Étape 2
### être capable de lire le corpus, charger les `Doc` Spacy et appliquer un modèle

Essayer d'utiliser `typing` et des `dataclass` pour structurer votre code

- partir du texte brut
- imposer la tokenisation de sequoia
    - cf. https://spacy.io/usage/linguistic-features#own-annotations
    - ou cf. https://spacy.io/api/doc
    - Quelles différences ?

## Étape 3
### quantifier les résultats 

- exactitude 
    - % de tags corrects
    - idem en distanguant les OOV
        - token.is_oov pour les embeddings
        - par rapport au train de sequoia
- vitesse 
    - bash `time`
    - module python `timeit`
    - comment améliorer ces temps ?
- Matrice de confusion
    (si on a le temps)
- comparer
    - différents modèles spacy
    - différents corpus UD

- consommation énergétique avec `pyJoules`
  Attention: `sudo chmod -R a+r /sys/class/powercap/intel-rapl` nécessaire
