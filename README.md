# TP - entrainement - Polonais

## Étape 5 : refaire la même chose sur d'autres langues

# POLONAIS

- [x] Télécharger le corpus conllu (train, dev et test) pour le polonais.
  - Premier essai sur le corpus pl-pdb-ud mais trop grand.
  - Deuxième essai sur le corpus pl-lfg-ud (corpus plus petit).
- [x] Convertir le corpus en corpus d'entrainement.
  > COMMANDES :

### Essai 1

`python3 -m spacy convert corpus_polonais/corpus-pdb/pl_pdb-ud-train.conllu corpus_polonais/corpus-ent`

`python3 -m spacy convert corpus_polonais/corpus-pdb/pl_pdb-ud-dev.conllu corpus_polonais/corpus-ent `

`python3 -m spacy convert corpus_polonais/corpus-pdb/pl_pdb-ud-test.conllu corpus_polonais/corpus-ent`

### Essai 2

`python3 -m spacy convert corpus_polonais/corpus-lfg/pl_lfg-ud-train.conllu corpus_polonais/corpus-ent`

`python3 -m spacy convert corpus_polonais/corpus-lfg/pl_lfg-ud-dev.conllu corpus_polonais/corpus-ent`

`python3 -m spacy convert corpus_polonais/corpus-lfg/pl_lfg-ud-test.conllu corpus_polonais/corpus-ent`

- [x] Configuration de la pipeline.
  > COMMANDE :

### Essai 1 (tagger)

`python3 -m spacy init fill-config ./config-pl/base_config.cfg config-pl/config.cfg`

### Essai 2 (morphologizer)

`python3 -m spacy init fill-config ./config-pl/base_config.cfg config-pl/config.cfg`

- [x] Entrainement.
  > COMMANDE

### Essai 1

`python3 -m spacy train ./config-pl/config.cfg --output ./model-pl/spacy_model2/ --paths.train ./corpus_polonais/corpus-ent/pl_pdb-ud-train.spacy --paths.dev ./corpus_polonais/corpus-ent/pl_pdb-ud-dev.spacy `

### Essai 2

`python3 -m spacy train ./config-pl/config.cfg --output ./model-pl/spacy_model2/ --paths.train ./corpus_polonais/corpus-ent/pl_lfg-ud-train.spacy --paths.dev ./corpus_polonais/corpus-ent/pl_lfg-ud-dev.spacy`

> RÉSULTATS

### Essai 1

```
================ Initializing pipeline =================
✔ Initialized pipeline

=================== Training pipeline ==================
ℹ Pipeline: ['tok2vec', 'tagger']
ℹ Initial learn rate: 0.001
E    #       LOSS TOK2VEC  LOSS TAGGER  TAG_ACC  SCORE
---  ------  ------------  -----------  -------  ------
  0       0          0.00        81.12    15.97    0.16
  0     200        275.80     12415.43    53.77    0.54
  0     400        628.09     11012.11    67.08    0.67
  0     600        867.87     11102.66    73.42    0.73
  ....
 38   12400       3266.91      4654.40    87.41    0.87
 39   12600       3288.62      4601.40    87.38    0.87
```

### Essai 2

```
===================== Initializing pipeline ========================
✔ Initialized pipeline

===================== Training pipeline ============================
ℹ Pipeline: ['tok2vec', 'morphologizer']
ℹ Initial learn rate: 0.001
E    #       LOSS TOK2VEC  LOSS MORPH...  POS_ACC  MORPH_ACC  SCORE
---  ------  ------------  -------------  -------  ---------  ------
  0       0          0.00          89.26    35.94      23.52    0.30
  0     200        265.81       12244.41    76.92      56.51    0.67
  0     400        573.08       10735.36    86.92      69.39    0.78
  0     600        783.52       10807.86    90.35      75.66    0.83
  1     800        906.72       10922.91    92.28      78.71    0.85
  1    1000       1074.28       11084.38    92.99      80.45    0.87
  2    1200       1268.32       11660.49    93.68      81.85    0.88
  2    1400       1481.75       11764.16    94.08      82.58    0.88
  3    1600       1561.41       11017.67    94.36      83.41    0.89
  4    1800       1745.80       10756.76    94.21      83.72    0.89
  6    2000       1847.81        9913.04    94.45      84.24    0.89
  7    2200       1848.48        8797.38    94.56      84.37    0.89
  9    2400       1887.62        8087.74    94.56      84.38    0.89
 11    2600       1675.37        6614.93    94.72      84.40    0.90
 13    2800       1539.89        5688.17    94.51      84.63    0.90
 15    3000       1425.24        4970.85    94.45      84.53    0.89
 17    3200       1331.20        4426.24    94.74      84.83    0.90
 19    3400       1248.32        4011.05    94.53      84.71    0.90
 21    3600       1187.69        3700.90    94.59      84.65    0.90
 22    3800       1115.90        3384.87    94.51      84.48    0.89
 24    4000       1029.13        3023.46    94.60      84.70    0.90
 26    4200       1020.63        2899.06    94.62      84.93    0.90
 28    4400        955.57        2663.25    94.63      84.88    0.90
 30    4600        938.47        2531.77    94.67      84.88    0.90
 32    4800        927.07        2457.63    94.61      84.76    0.90
✔ Saved pipeline to output directory
model-pl/spacy_model2/model-last
```

- [x] Évaluation.
  > COMMANDE
  > `python3 scripts/eval-polonais.py`

> RÉSULTATS

### Essai 1

```
./model-pl/spacy_model2/model-best
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1471: UndefinedMetricWarning: Recall and F-score are ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1471: UndefinedMetricWarning: Recall and F-score are ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1471: UndefinedMetricWarning: Recall and F-score are ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, msg_start, len(result))
```

```
                                  precision    recall  f1-score   support

                             ADJ       0.00      0.00      0.00       0.0
                             ADP       0.00      0.00      0.00       0.0
                             ADV       0.00      0.00      0.00       0.0
                             AUX       0.00      0.00      0.00       0.0
                           CCONJ       0.00      0.00      0.00       0.0
                             DET       0.00      0.00      0.00       0.0
                            INTJ       0.00      0.00      0.00       0.0
                            NOUN       0.00      0.00      0.00       0.0
                             NUM       0.00      0.00      0.00       0.0
                            PART       0.00      0.00      0.00       0.0
                            PRON       0.00      0.00      0.00       0.0
                           PROPN       0.00      0.00      0.00       0.0
                           PUNCT       0.00      0.00      0.00       0.0
                           SCONJ       0.00      0.00      0.00       0.0
                             SYM       0.00      0.00      0.00       0.0
                            VERB       0.00      0.00      0.00       0.0
                               X       0.00      0.00      0.00       0.0
                adj:pl:acc:f:com       0.00      0.00      0.00       1.0
                adj:pl:gen:n:pos       0.00      0.00      0.00      71.0
                adj:sg:nom:n:sup       0.00      0.00      0.00       4.0
                            adja       0.00      0.00      0.00      22.0
                            adjc       0.00      0.00      0.00       2.0
                        adjp:dat       0.00      0.00      0.00       9.0
                        adjp:gen       0.00      0.00      0.00       2.0
                              ...
         ger:sg:dat:n:imperf:aff       0.00      0.00      0.00       2.0
           ger:sg:dat:n:perf:aff       0.00      0.00      0.00       1.0
             winien:sg:m3:imperf       0.00      0.00      0.00       5.0
              winien:sg:n:imperf       0.00      0.00      0.00       1.0

                        accuracy                           0.00   33616.0
                       macro avg       0.00      0.00      0.00   33616.0
                    weighted avg       0.00      0.00      0.00   33616.0

pl_core_news_sm
              precision    recall  f1-score   support

         ADJ       0.97      0.95      0.96      3424
         ADP       1.00      0.99      1.00      3546
         ADV       0.92      0.90      0.91      1114
         AUX       0.70      0.88      0.78       668
       CCONJ       0.97      0.91      0.94      1099
         DET       0.96      0.97      0.97       847
        INTJ       0.46      0.75      0.57         8
        NOUN       0.95      0.97      0.96      8406
         NUM       0.93      0.95      0.94       253
        PART       0.84      0.95      0.89       935
        PRON       0.99      0.98      0.98      1598
       PROPN       0.86      0.85      0.85      1171
       PUNCT       1.00      1.00      1.00      5632
       SCONJ       0.94      0.95      0.95       684
         SYM       0.25      0.33      0.29         3
        VERB       0.96      0.97      0.96      3865
           X       0.78      0.23      0.35       363

    accuracy                           0.96     33616
   macro avg       0.85      0.85      0.84     33616
weighted avg       0.96      0.96      0.95     33616

pl_core_news_md
              precision    recall  f1-score   support

         ADJ       0.98      0.97      0.97      3393
         ADP       1.00      1.00      1.00      3537
         ADV       0.94      0.93      0.93      1111
         AUX       0.71      0.90      0.79       659
       CCONJ       0.97      0.91      0.94      1095
         DET       0.96      0.98      0.97       841
        INTJ       0.31      0.67      0.42         6
        NOUN       0.96      0.98      0.97      8353
         NUM       0.96      0.95      0.95       262
        PART       0.86      0.96      0.90       945
        PRON       0.98      0.96      0.97      1633
       PROPN       0.88      0.87      0.88      1168
       PUNCT       1.00      1.00      1.00      5632
       SCONJ       0.95      0.95      0.95       688
         SYM       0.50      0.50      0.50         4
        VERB       0.98      0.98      0.98      3860
           X       0.83      0.21      0.33       429

    accuracy                           0.96     33616
   macro avg       0.87      0.86      0.85     33616
weighted avg       0.96      0.96      0.96     33616

pl_core_news_lg
              precision    recall  f1-score   support

         ADJ       0.98      0.97      0.98      3408
         ADP       1.00      1.00      1.00      3535
         ADV       0.93      0.92      0.93      1110
         AUX       0.70      0.89      0.79       663
       CCONJ       0.97      0.91      0.94      1100
         DET       0.96      0.98      0.97       842
        INTJ       0.46      0.67      0.55         9
        NOUN       0.97      0.98      0.97      8369
         NUM       0.96      0.94      0.95       263
        PART       0.85      0.96      0.90       938
        PRON       0.98      0.97      0.98      1606
       PROPN       0.92      0.87      0.89      1217
       PUNCT       1.00      1.00      1.00      5630
       SCONJ       0.95      0.95      0.95       689
         SYM       0.50      0.40      0.44         5
        VERB       0.98      0.99      0.98      3849
           X       0.83      0.23      0.36       383

    accuracy                           0.96     33616
   macro avg       0.88      0.86      0.86     33616
weighted avg       0.97      0.96      0.96     33616
```

### Essai 2

./model-pl/spacy_model2/model-best
precision recall f1-score support

         ADJ       0.90      0.91      0.91       817
         ADP       0.99      0.97      0.98      1123
         ADV       0.95      0.90      0.93       625
         AUX       0.56      0.92      0.69       260
       CCONJ       0.99      0.89      0.94       393
         DET       0.90      0.95      0.92       305
        INTJ       0.33      0.50      0.40         4
        NOUN       0.94      0.92      0.93      2526
         NUM       0.91      0.94      0.93        87
        PART       0.95      0.97      0.96       586
        PRON       0.98      0.97      0.98       998
       PROPN       0.86      0.89      0.88       453
       PUNCT       1.00      1.00      1.00      2564
       SCONJ       0.99      0.92      0.96       152
        VERB       0.96      0.95      0.96      2219

    accuracy                           0.95     13112

macro avg 0.88 0.91 0.89 13112
weighted avg 0.95 0.95 0.95 13112

pl_core_news_sm
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
precision recall f1-score support

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

macro avg 0.83 0.84 0.83 13112
weighted avg 0.95 0.95 0.95 13112

pl_core_news_md
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
precision recall f1-score support

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

macro avg 0.85 0.87 0.85 13112
weighted avg 0.95 0.96 0.95 13112

pl_core_news_lg
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sklearn/metrics/\_classification.py:1471: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
\_warn_prf(average, modifier, msg_start, len(result))
precision recall f1-score support

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

macro avg 0.84 0.85 0.84 13112
weighted avg 0.96 0.96 0.96 13112

# ARABE

- [ ] Télécharger le corpus conllu (train, dev et test) pour l'arabe.
- [ ] Convertir le corpus en corpus d'entrainement.

  > COMMANDES :

- [ ] Configuration de la pipeline. (tagger + morphologizer)
  > COMMANDE :

`python3 -m spacy init fill-config config-ar/base_config.cfg config-ar/config.cfg`

- [ ] Entrainement.
  > COMMANDE :

> RÉSULTATS

- [ ] Évaluation.
  > COMMANDE

`python3 scripts/eval-arabe.py`

> RÉSULTATS
