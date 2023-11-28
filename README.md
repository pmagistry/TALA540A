# TALA540A : TP de Laura Darenne

## to-do-list
- [] : passer d'un modèle spacy effiency à accuracy : https://spacy.io/usage/training#quickstart

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
- heuresement data déjà splittée  deonc pas besoin

- mon modèle 1 : entrainement caractère par caractère
- => modèle tout petit par rapport au modèle original

```shell
(project) laura@laura:~/Documents/TALA540A$ python models/train_jiayan.py 
Building data...
Training...
{'num': 50, 'scores': {}, 'loss': 179224.645238, 'feature_norm': 238.066439, 'error_norm': 1643.158008, 'active_features': 8595, 'linesearch_trials': 1, 'linesearch_step': 1.0, 'time': 0.438}
/home/laura/miniconda3/envs/project/lib/python3.11/site-packages/sklearn/metrics/_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
              precision    recall  f1-score   support

         ADP    0.82375   0.74266   0.78111       579
         ADV    0.82021   0.67526   0.74071      2716
         AUX    0.64897   0.94386   0.76912       570
       CCONJ    0.96893   1.00000   0.98422       499
        INTJ    0.71429   0.41667   0.52632        12
        NOUN    0.86426   0.87003   0.86713      7040
         NUM    0.98918   0.97859   0.98385       467
        PART    0.92770   0.90230   0.91483      1607
        PRON    0.89273   0.61817   0.73050      1629
       PROPN    0.88709   0.72204   0.79610      3112
       SCONJ    0.53191   1.00000   0.69444       600
         SYM    0.00000   0.00000   0.00000         1
        VERB    0.78516   0.85906   0.82045      8734

   micro avg    0.82330   0.82330   0.82330     27566
   macro avg    0.75802   0.74836   0.73914     27566
weighted avg    0.83419   0.82330   0.82290     27566
 samples avg    0.82330   0.82330   0.82330     27566

```

- mon module 2 : avec corpus par phrase et non par caractère
- => modèle plus grand que module 1, mais toujours tout petit par rapport au modèle original
```shell
(project) laura@laura:~/Documents/TALA540A$ python models/train_jiayan.py 
Building data...
Training...
{'num': 50, 'scores': {}, 'loss': 96350.669375, 'feature_norm': 256.382022, 'error_norm': 659.339159, 'active_features': 52299, 'linesearch_trials': 1, 'linesearch_step': 1.0, 'time': 1.313}
/home/laura/miniconda3/envs/project/lib/python3.11/site-packages/sklearn/metrics/_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
              precision    recall  f1-score   support

         ADP    0.89073   0.92919   0.90955       579
         ADV    0.87579   0.87224   0.87401      2716
         AUX    0.85191   0.89825   0.87447       570
       CCONJ    0.98812   1.00000   0.99402       499
        INTJ    1.00000   0.33333   0.50000        12
        NOUN    0.89602   0.92784   0.91165      7040
         NUM    0.98913   0.97430   0.98166       467
        PART    0.96744   0.96142   0.96442      1607
        PRON    0.94717   0.91344   0.93000      1629
       PROPN    0.92804   0.83708   0.88022      3112
       SCONJ    0.94318   0.96833   0.95559       600
         SYM    0.00000   0.00000   0.00000         1
        VERB    0.88860   0.89592   0.89225      8734

   micro avg    0.90521   0.90521   0.90521     27566
   macro avg    0.85893   0.80857   0.82060     27566
weighted avg    0.90574   0.90521   0.90501     27566
 samples avg    0.90521   0.90521   0.90521     27566
```

---

## test à faire

- tableau de conversions, en fonction de :
  - papier
  - analyse quantitative
  - analyse qualitative

- test avec ou sans ponctuations
=> trouver un ponctuateur

- test pour tableau de conversion avec ou sans i,j