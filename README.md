 TALA540A : TP de Laura Darenne

## to-do-list
- [] : changer confusion matrix = refaire comme au départ
- [] : modifier la partie evaluations de jiayan
- [] : modifier la partie evaluations de spacy

---

## liste des fichiers
- README.md : explications des fichiers

### dossier corpus
- allpos_corpus : corpus pour train module jiayan
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
- evaluate_jiayan.py : fichier python pour évaluer les modèles jiayan
- get_evaluation_jiayan.py : fichier python contenant les fonctions pour l'évaluation des pos-tagging des modèles jiayan
- get_corpus.py : fichier python contenant les fonctions pour obtenir les corpus tokenisés

### models
- dossier jiayan : contient les modèles jiayan
- dossier spacy : contient notre modèle spacy et les fichiers config
- train_jiayan.py : pour entrainer mon propre module jiayan
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

- entrainement utilise random.shuffle() `=> Deprecated since version 3.9, removed in version 3.11: The optional parameter random`
- heureusement data déjà splittée  deonc pas besoin

- mon modèle 1 : entrainement caractère par caractère
- => modèle tout petit par rapport au modèle original

- mon module 2 : avec corpus par phrase et non par caractère
- => modèle plus grand que module 1, mais toujours tout petit par rapport au modèle original

---

## test à faire

- tableau de conversions, en fonction de :
  - papier
  - analyse quantitative
  - analyse qualitative
  - test pour tableau de conversion avec ou sans i,j

- modèles jiayan :
  - mot par mot
  - table par table
  - phrase par phrase

- modèles spacy, évaluer en fonction des vecteurs (potentiellement prendre petit batch pour influer sur la loss mais ne pas se prendre la tête) :
  - taille contexte plus ou moins grand ; 
  - taille dimension vecteur ; 
  - modifier corpus (recoller phrase) / ou texte classique brut avec tokenisation caractère = mot trouvé sur internet