# TALA540A : TP de Laura Darenne

## liste des fichiers
- README.md : explications du tp
- TP_entrainement.md : étapes du tp à faire

#### ./script
- get_corpus.py : fichier python contenant les fonctions appelées par tp1.py pour obtenir les corpus tokenisés
- get_evaluation.py : fichier python contenant les fonctions appelées par tp1.py pour l'évaluation des tokenisations
- datastructures.py : fichier python contenant les dataclasses 

- tp2.py : fichier python principal pour le TP2
- corpus.sh : fichier bash pour transformer les fichiers conllu en fichier spacy
- spacy
	- fr_sequoia-ud-dev.spacy
	- fr_sequoia-ud-train.spacy
- model_fr et model_zh : nos modèles entrainés
	- model-best : le modèle que l'on prend pour chaque langue

#### ./corpus
- corpus français :
	- fr_sequoia-ud-test.conllu
	- fr_sequoia-ud-train.conllu
	- fr_sequoia-ud-dev.conllu
- corpus chinois :
	- zh_pud-ud-test.conllu

---

## TP_entrainement

### étape 1 : préparation du corpus

- [x] fichier dev train sous format spacy pour sequoia
- [ ] seulement des fichiers test pour le chinois, à voir plus tard

### étape 2 : configuration de la pipeline

Premier modele à télécharger sous forme `base_config.cfg`
- language : french
- components : tagger
- hardware : cpu
- optimize for : efficiency

```shell
(project) laura@laura:~/Documents/TALA540A/script$ python -m spacy init fill-config base_config.cfg config.cfg
✔ Auto-filled config with all values
✔ Saved config
config.cfg
You can now add your data and train your pipeline:
python -m spacy train config.cfg --paths.train ./train.spacy --paths.dev ./dev.spacy
```

On modifie `base.cfg` pour accélérer l'entraînement et voir que tout fonctionne
- batch_size : train petit donc on test 100
- max_steps : 20000 (valeur laissée par défaut)
- max_epochs : on teste 20

### étape 3: entraînement

```shell
(project) laura@laura:~/Documents/TALA540A/script$ python -m spacy train config.cfg --output ./model_fr/ --paths.train ./spacy/fr_sequoia-ud-train.spacy --paths.dev ./spacy/fr_sequoia-ud-dev.spacy
✔ Created output directory: model_fr
ℹ Saving to output directory: model_fr
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
model_fr/model-last
```

### étape 4: évaluation

Je tente de load le modèle comme ceci
```python
nlp = spacy.load("./script/model_fr/model-best")
```
Mais petit problème ...
```shell
(project) laura@laura:~/Documents/TALA540A$ python script/tp2.py 
phrases conllu: 100%|██████████████████████| 456/456 [00:00<00:00, 32681.21it/s]
phrases spacy: 100%|█████████████████████████| 456/456 [00:02<00:00, 168.15it/s]
L'accuracy est à 0.0%.
En tenant compte du vocabulaire, l'accuracy est à 0.0%.
```

### étape 5: refaire la même chose sur un autre langue/d'autres corpus