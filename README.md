# TALA540A : TP de Laura Darenne

## to-do-list
- [] : entrainer en divisant le corpus

## liste des fichiers
- README.md : explications du tp

#### ./script
- get_corpus.py et get_spacy.py : fichier python contenant les fonctions appelées par 2_evaluation.py pour obtenir les corpus tokenisés
- get_evaluation.py : fichier python contenant les fonctions appelées par 2_evaluation.py pour l'évaluation des tokenisations
- datastructures.py : fichier python contenant les dataclasses 
- 2_evaluation.py : fichier python principal pour le TP2

- 1_train_spacy.sh : fichier bash pour transformer les fichiers conllu en fichier spacy et lancer le train
- model_spacy
  - corpus
  	- lzh_kyoto-ud-dev.spacy
    - lzh_kyoto-ud-train.spacy
- monmodel : mon modèle entrainé
	- model-best : le modèle que l'on prend pour l'évaluation

#### ./corpus
- lzh_kyoto-ud-dev.conllu
- lzh_kyoto-ud-test.conllu
- lzh_kyoto-ud-train.conllu
- xpos.py : pour modifier les corpus si besoin pour l'entrainement du modèle spacy