# TP 2 SANDRA JAGODZINSKA

## corpus
- nous avons pris pour le projet finale corpus ud_lfg qui n'était pas utilisé pour entraîner le modèle spacy (NKJP et UD-PDB étaient utilisés)

## tous ce que je devrais faire si j'ai du temps

- [] diviser les corpus à partir de conllu
- [X] entraînement en polonais : XPOS avec des traits morpho plus fines, alors lancer morphologizer
- [] trouver comment entrainer treeTagger (car sur siteweb ils disent que c'est possible mais personne mentionne comment :))) )
- [] essayer avec des vecteurs

## entraînement

### 1. La métamorphose de fichiers conllu en fichier entrainement spacy

### 2. La configuration de pipeline
#### 2.1 La configuration de pipeline en utilisant morphologizer au lieu de tagger
- fichier `base_config_polonais.cfg`
- commande `python3 -m spacy init fill-config base_config_polonais.cfg config_polonais.cfg`
-fichier `config_polonais.cfg`
- lancement d'entraînement resultats en 3.1
#### 2.2 La configuration de pipeline en utilisant morpho au lieu de tagger + accuracy au lieu de efficiency
- fichier `base_config_pl_acc.cfg `
- commande `python3 -m spacy init fill-config base_config_pl_acc.cfg config_pl_acc.cfg`
- fichier `config_pl_acc.cfg`
- lancement d'entraînement resultats en 3.2

#### 3.1
```
✔ Created output directory: spacy_model_pl
ℹ Saving to output directory: spacy_model_pl
ℹ Using CPU
ℹ To switch to GPU 0, use the option: --gpu-id 0

=========================== Initializing pipeline ===========================
✔ Initialized pipeline

============================= Training pipeline =============================
ℹ Pipeline: ['tok2vec', 'morphologizer']
ℹ Initial learn rate: 0.001
E    #       LOSS TOK2VEC  LOSS MORPH...  POS_ACC  MORPH_ACC  SCORE 
---  ------  ------------  -------------  -------  ---------  ------
 65    8200        685.14        1322.07    94.80      85.13    0.90
 67    8400        653.85        1255.57    94.63      85.18    0.90
 69    8600        696.03        1295.47    94.70      85.05    0.90
 71    8800        655.56        1207.34    94.69      84.92    0.90
 72    9000        661.12        1192.93    94.62      84.84    0.90
 74    9200        656.61        1161.97    94.75      85.14    0.90
 76    9400        664.28        1168.94    94.61      85.09    0.90
 78    9600        659.82        1147.67    94.80      85.05    0.90
 80    9800        648.95        1104.27    94.72      85.02    0.90
✔ Saved pipeline to output directory
spacy_model_pl/model-last```

#### 3.2

```
OSError: [E884] The pipeline could not be initialized because the vectors could not be found at 'pl_core_news_lg'. If your pipeline was already initialized/trained before, call 'resume_training' instead of 'initialize', or initialize only the components that are new.
```
- je ne comprends pas l'erreur

## évaluation des modèles 

```
MacBook-Pro-Sandra:TALA540A sandrajagodzinska$ python3 eval_basique.py
WARNING:root:pynvml not found you can't use NVIDIA devices
spacy_model_pl/model-best
(0.9495118974984746, 0.8604651162790697)
pl_core_news_sm
(0.949359365466748, 0.9143206854345165)
pl_core_news_md
(0.9553843807199512, 0.9367605059159527)
pl_core_news_lg
(0.9576723611958511, 0.941656466748266)

_______________

spacy_model_pl/model-best

              precision    recall  f1-score   support

         ADJ       0.90      0.93      0.92       811
         ADP       1.00      0.94      0.97      1165
         ADV       0.96      0.90      0.93       629
         AUX       0.55      0.92      0.69       259
       CCONJ       0.99      0.97      0.98       360
         DET       0.92      0.96      0.94       310
        INTJ       0.33      1.00      0.50         2
        NOUN       0.94      0.92      0.93      2516
         NUM       0.94      0.96      0.95        89
        PART       0.97      0.94      0.95       615
        PRON       0.99      0.98      0.98       993
       PROPN       0.82      0.90      0.86       429
       PUNCT       1.00      1.00      1.00      2556
       SCONJ       0.99      0.93      0.96       150
        VERB       0.97      0.95      0.96      2228

    accuracy                           0.95     13112
   macro avg       0.89      0.95      0.90     13112
weighted avg       0.96      0.95      0.95     13112

pl_core_news_sm


              precision    recall  f1-score   support

         ADJ       0.96      0.95      0.95       842
         ADP       0.99      0.99      0.99      1101
         ADV       0.93      0.93      0.93       586
         AUX       0.53      0.79      0.64       289
       CCONJ       0.95      0.95      0.95       353
         DET       0.95      0.97      0.96       317
        INTJ       0.33      0.40      0.36         5
        NOUN       0.96      0.94      0.95      2512
         NUM       0.94      0.99      0.97        86
        PART       0.93      0.93      0.93       600
        PRON       0.99      0.98      0.98       995
       PROPN       0.87      0.81      0.84       503
       PUNCT       1.00      1.00      1.00      2556
       SCONJ       0.99      0.87      0.92       160
        VERB       0.94      0.96      0.95      2142
           X       0.00      0.00      0.00        65

    accuracy                           0.95     13112
   macro avg       0.83      0.84      0.83     13112
weighted avg       0.95      0.95      0.95     13112

pl_core_news_md
              precision    recall  f1-score   support

         ADJ       0.96      0.94      0.95       850
         ADP       0.99      0.99      0.99      1098
         ADV       0.92      0.95      0.93       574
         AUX       0.55      0.79      0.64       298
       CCONJ       0.95      0.96      0.96       352
         DET       0.95      0.96      0.96       321
        INTJ       0.50      0.75      0.60         4
        NOUN       0.97      0.96      0.97      2466
         NUM       0.99      0.98      0.98        91
        PART       0.95      0.93      0.94       605
        PRON       0.99      0.96      0.97      1015
       PROPN       0.90      0.87      0.89       488
       PUNCT       1.00      1.00      1.00      2555
       SCONJ       0.99      0.87      0.92       160
        VERB       0.96      0.98      0.97      2134
           X       0.00      0.00      0.00       101

    accuracy                           0.96     13112
   macro avg       0.85      0.87      0.85     13112
weighted avg       0.95      0.96      0.95     13112

pl_core_news_lg

              precision    recall  f1-score   support

         ADJ       0.97      0.95      0.96       849
         ADP       0.99      0.99      0.99      1098
         ADV       0.93      0.94      0.94       581
         AUX       0.54      0.78      0.64       298
       CCONJ       0.97      0.97      0.97       353
         DET       0.96      0.97      0.96       322
        INTJ       0.33      0.40      0.36         5
        NOUN       0.97      0.96      0.97      2480
         NUM       0.98      0.98      0.98        90
        PART       0.94      0.95      0.94       595
        PRON       0.99      0.98      0.98       994
       PROPN       0.91      0.83      0.87       517
       PUNCT       1.00      1.00      1.00      2555
       SCONJ       0.99      0.87      0.93       159
        VERB       0.96      0.98      0.97      2140
           X       0.00      0.00      0.00        76

    accuracy                           0.96     13112
   macro avg       0.84      0.85      0.84     13112
weighted avg       0.96      0.96      0.96     13112


```

