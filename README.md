# TALA540A : TP de Laura Darenne

## to-do-list
- [] : entrainer en divisant le corpus ?
- [x] : résoudre problème tagging avec corpus chinois :
  - spacy prend les XPOS pour le tagging au lieu des UPOS
  - => j'ai copié collé avec grep les UPOS dans la colonne XPOS

## liste des fichiers
- README.md : explications du tp
- TP_entrainement.md : étapes du tp à faire

#### ./script
- get_conllu.py et get_spacy.py : fichier python contenant les fonctions appelées par tp1.py pour obtenir les corpus tokenisés
- get_evaluation.py : fichier python contenant les fonctions appelées par tp1.py pour l'évaluation des tokenisations
- datastructures.py : fichier python contenant les dataclasses 
- tp2.py : fichier python principal pour le TP2

- corpus_and_train.sh : fichier bash pour transformer les fichiers conllu en fichier spacy et lancer le train
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
- xpos.py : pour modif sur corpus si besoin pour l'entrainement du modèle spacy, pas mis à jour depuis tp entrainement, suppression prochaine peut-être