 TALA540A : TP de Laura Darenne

## corpus

- liste des sous-corpus
KR1h0001
KR1h0004
KR1d0052
KR2b0041
KR2e0003
KR4a0001
KR4h0169
KR6c0127
KR6c0023
KR6f0082

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

## word2vec

### table
1 Word2Vec(sentences=sentences, vector_size=100, window=3, min_count=1, workers=4)
2 Word2Vec(sentences=sentences, vector_size=50, window=3, min_count=1, workers=4)
3 Word2Vec(sentences=sentences, vector_size=200, window=3, min_count=1, workers=4)
4 Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
5 Word2Vec(sentences=sentences, vector_size=100, window=10, min_count=1, workers=4)

### sentence
6 Word2Vec(sentences=sentences, vector_size=100, window=3, min_count=1, workers=4)
7 Word2Vec(sentences=sentences, vector_size=50, window=3, min_count=1, workers=4)
8 Word2Vec(sentences=sentences, vector_size=200, window=3, min_count=1, workers=4)
9 Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
10 Word2Vec(sentences=sentences, vector_size=100, window=10, min_count=1, workers=4)