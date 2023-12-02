# TP 2 SANDRA JAGODZINSKA

## corpus
- nous avons pris pour le projet finale corpus ud_lfg qui n'était pas utilisé pour entraîner le modèle spacy (NKJP et UD-PDB étaient utilisés)

## tous ce que je devrais faire si j'ai du temps

- [X] diviser les corpus à partir de conllu
- [X] entraînement en polonais : XPOS avec des traits morpho plus fines, alors lancer morphologizer
- [] trouver comment entrainer treeTagger (car sur siteweb ils disent que c'est possible mais personne mentionne comment :))) )
- [] essayer avec des vecteurs

## entraînement

### 1. La métamorphose de fichiers conllu en fichier entrainement spacy
- modifications de fonction read conllu dans le fichier eval_basique.py pour récupérer automatiquement les sous-corpus du corpus polonais lfg 

### 2. La configuration de pipeline
#### 2.1 La configuration de pipeline en utilisant morphologizer au lieu de tagger
- fichier `base_config_polonais.cfg`
- commande `python3 -m spacy init fill-config base_config_polonais.cfg config_polonais.cfg`
- fichier `config_polonais.cfg`
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
spacy_model_pl/model-last 
```

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

news
(0.9537947997189037, 0.8707317073170732)
fiction
(0.944892252015134, 0.8514285714285714)
(media)
(0.9538461538461539, 0.8571428571428571)
social
(0.9494949494949495, 0.8235294117647058)
(conversational)
(0.9336188436830836, 0.7954545454545454)
nonfiction
(0.9301310043668122, 0.834061135371179)
(prepared)
(0.9707446808510638, 0.8571428571428571)
legal
(1.0, 1.0)
blog
(0.9826086956521739, 0.9629629629629629)
academic
(0.8181818181818182, 0.3333333333333333)


pl_core_news_sm
(0.949359365466748, 0.9143206854345165)

news
(0.9567814476458187, 0.9219512195121952)
fiction
(0.9416022372100674, 0.9057142857142857)
(media)
(0.9384615384615385, 1.0)
social
(0.9528619528619529, 0.9607843137254902)
(conversational)
(0.9357601713062098, 0.8409090909090909)
nonfiction
(0.9362445414847161, 0.9170305676855895)
(prepared)
(0.976063829787234, 0.9142857142857143)
legal
(1.0, 1.0)
blog
(0.9565217391304348, 0.8888888888888888)
academic
(0.9090909090909091, 1.0)



pl_core_news_md
(0.9553843807199512, 0.9367605059159527)

news
(0.9634574841883345, 0.9390243902439024)
fiction
(0.9485112683007073, 0.9352380952380952)
(media)
(0.9384615384615385, 1.0)
social
(0.9663299663299664, 0.9803921568627451)
(conversational)
(0.9357601713062098, 0.8636363636363636)
nonfiction
(0.9423580786026201, 0.9170305676855895)
(prepared)
(0.976063829787234, 1.0)
legal
(1.0, 1.0)
blog
(0.9304347826086956, 0.8518518518518519)
academic
(0.7272727272727273, 0.6666666666666666)


pl_core_news_lg
(0.9576723611958511, 0.941656466748266)

(0.9576723611958511, 0.941656466748266)
news
(0.9660927617709065, 0.9479674796747968)
fiction
(0.9506497779240006, 0.9361904761904762)
(media)
(0.9384615384615385, 1.0)
social
(0.9562289562289562, 0.9803921568627451)
(conversational)
(0.9400428265524625, 0.8863636363636364)
nonfiction
(0.9475982532751092, 0.9301310043668122)
(prepared)
(0.9787234042553191, 0.9714285714285714)
legal
(1.0, 1.0)
blog
(0.9478260869565217, 0.8518518518518519)
academic
(0.7272727272727273, 0.6666666666666666)


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

