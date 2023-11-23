# TALA540A : TP de Laura Darenne

## to-do-list
- [] : finaliser choix du tagger pos pour chinois classique
- [] : passer d'un modèle spacy effiency à accuracy : https://spacy.io/usage/training#quickstart

## liste des fichiers
- README.md : explications du tp

### ./script
- 1a_train_spacy.sh : fichier bash pour transformer les fichiers conllu en fichier spacy et lancer le train
- 1b_extract.corpus.py : fichier python pour extraire un sous-corpus au choix du corpus principal
- 2_evaluation.py : fichier python pour évaluer tous les modèles
- get_corpus.py : fichier python contenant les fonctions pour obtenir les corpus tokenisés
- get_evaluation.py : fichier python contenant les fonctions pour l'évaluation des pos-tagging
- datastructures.py : fichier python contenant les dataclasses 

- model_spacy
  - corpus : fichiers spacy
  - monmodel : mon modèle entrainé
    - model-best : le modèle que l'on prend pour l'évaluation
- model jiayan : https://github.com/jiaeyan/Jiayan/tree/master

### ./corpus
- lzh_kyoto-ud-dev.conllu
- lzh_kyoto-ud-test.conllu
- lzh_kyoto-ud-train.conllu
- xpos.py : pour modifier les corpus si besoin pour l'entrainement du modèle spacy