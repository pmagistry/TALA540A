# TALA540A : TP de Laura Darenne

## to-do-list
- [] : passer d'un modèle spacy effiency à accuracy : https://spacy.io/usage/training#quickstart
- [] : jiayan - entrainer module crf

---

## liste des fichiers
- README.md : explications des fichiers

### dossier corpus
- allpos_corpus : corpus pour train moduel crf
- old_corpus : corpus kyoto original   
- sous_corpus : sous-corpus extraits à l'aide du fichier `extract_sous_corpus.py`
- spacy_corpus : corpus spacy obtenu à l'aide du fichier `./models/train_spacy.sh`

- lzh_kyoto-ud-dev.conllu
- lzh_kyoto-ud-test.conllu
- lzh_kyoto-ud-train.conllu  

- extract.py : pour modifier le corpus original
- extract_sous_corpus.py : pour extraire des sous-corpus
- => les deux fichiers python s'appellent directement dans le dossier corpus

### dossier evaluations
- datastructures.py : fichier python contenant les classes  
- evaluate_spacy.py : fichier python pour évaluer tous les modèles spacy
- get_evaluation_spacy.py : fichier python contenant les fonctions pour l'évaluation des pos-tagging des modèles spacy
- evaluate_jiayan.py : fichier python pour évaluer les modèles crf
- get_evaluation_jiayan.py : fichier python contenant les fonctions pour l'évaluation des pos-tagging des modèles crf
- get_corpus.py : fichier python contenant les fonctions pour obtenir les corpus tokenisés

### models
- dossier jiayan : contient les modèles crf
- dossier spacy : contient notre modèle spacy et les fichiers config
- train_jiayan.py : pour entrainer mon propre module crf
  - https://github.com/jiaeyan/Jiayan/tree/master
- train_spacy.sh : pour entrainer mon propre module spacy

### papiers

### ./script
- 1a_train_spacy.sh : fichier bash pour transformer les fichiers conllu en fichier spacy et lancer le train

---

## module jieyan
- installation modules
- pip install jiayan
- pip install https://github.com/kpu/kenlm/archive/master.zip
- télécharger models : https://drive.google.com/file/d/1piZQBO8OXQ5Cpi17vAcZsrbJLPABnKzp/view

---

## test à faire

- avec ou sans ponctuations