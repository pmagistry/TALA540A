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
  	- fr_sequoia-ud-dev.spacy
  	- fr_sequoia-ud-train.spacy
    - zh_gsdsimp-ud-dev.conllu
    - zh_gsdsimp-ud-train.spacy
- model_fr et model_zh : nos modèles entrainés
	- model-best : le modèle que l'on prend pour chaque langue

#### ./corpus
- fr_sequoia-ud-test.conllu
- fr_sequoia-ud-train.conllu
- fr_sequoia-ud-dev.conllu
- zh_gsdsimp-ud-test.conllu
- zh_gsdsimp-ud-train.conllu
- zh_gsdsimp-ud-dev.conllu

---

## TP_entrainement

### étape 1 : préparation du corpus

- corpus chinois gsd et corpus français sequoia

- division en sous-corpus possible pour sequoia mais pas pour gsd (car pas de sous-corpus)

### étape 2 : configuration de la pipeline

Premier modele à télécharger sous forme `base_config.cfg`
- language : french
- components : tagger
- hardware : cpu
- optimize for : efficiency

```shell
(project) laura@laura:~/Documents/TALA540A/script/model_spacy$ python -m spacy init fill-config base_config_fr.cfg config_fr.cfg
✔ Auto-filled config with all values
✔ Saved config
config_fr.cfg
You can now add your data and train your pipeline:
python -m spacy train config_fr.cfg --paths.train ./train.spacy --paths.dev ./dev.spacy
```

On modifie `config_fr.cfg` pour accélérer l'entraînement et voir que tout fonctionne
- batch_size : 100 valeur par défaut
- max_steps : 20000 (valeur laissée par défaut)
- max_epochs : on teste 20

### étape 3: entraînement
- je lance le script ./corpus_and_train.sh qui crée les fichiers corpus .spacy et lance le train

```shell
(project) laura@laura:~/Documents/TALA540A$ ./script/corpus_and_train.sh ./corpus/fr_sequoia-ud-train.conllu ./corpus/fr_sequoia-ud-dev.conllu ./script/model_spacy/corpus/ french
ℹ Grouping every 1 sentences into a document.
⚠ To generate better training data, you may want to group sentences
into documents with `-n 10`.
✔ Generated output file (2231 documents):
script/model_spacy/corpus/fr_sequoia-ud-train.spacy
ℹ Grouping every 1 sentences into a document.
⚠ To generate better training data, you may want to group sentences
into documents with `-n 10`.
✔ Generated output file (412 documents):
script/model_spacy/corpus/fr_sequoia-ud-dev.spacy
ℹ Saving to output directory: script/model_spacy/model_fr
ℹ Using CPU

=========================== Initializing pipeline ===========================
✔ Initialized pipeline

============================= Training pipeline =============================
ℹ Pipeline: ['tok2vec', 'tagger']
ℹ Initial learn rate: 0.001
E    #       LOSS TOK2VEC  LOSS TAGGER  TAG_ACC  SCORE 
---  ------  ------------  -----------  -------  ------
  0       0          0.00        66.37    28.19    0.28
  0     200        139.13      4809.94    89.04    0.89
  0     400        158.29      2286.60    91.90    0.92
  1     600        112.47      1497.87    92.94    0.93
  2     800        102.60      1359.98    93.27    0.93
  3    1000         72.72       955.74    93.46    0.93
  4    1200         49.49       669.60    93.73    0.94
  5    1400         37.44       529.17    93.68    0.94
  7    1600         28.61       433.86    93.68    0.94
  9    1800         19.91       315.78    93.68    0.94
 12    2000         17.34       287.01    93.71    0.94
 15    2200         12.46       214.40    93.69    0.94
 19    2400         10.03       180.60    93.70    0.94
✔ Saved pipeline to output directory
script/model_spacy/model_fr/model-last
```

### étape 4: évaluation

C'est bon !