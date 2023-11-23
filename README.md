# TP - entrainement - Polonais

## Étape 5 : refaire la même chose sur d'autres langues

# POLONAIS

- [x] Télécharger le corpus conllu (train, dev et test) pour le polonais.
- [x] Convertir le corpus en corpus d'entrainement.
  > COMMANDES :

`python3 -m spacy convert corpus_polonais/corpus-pdb/pl_pdb-ud-train.conllu corpus_polonais/corpus-ent`

`python3 -m spacy convert corpus_polonais/corpus-pdb/pl_pdb-ud-dev.conllu corpus_polonais/corpus-ent `

`python3 -m spacy convert corpus_polonais/corpus-pdb/pl_pdb-ud-test.conllu corpus_polonais/corpus-ent`

- [x] Configuration de la pipeline.
  > COMMANDE :

`python -m spacy init fill-config ./config-pl/base_config.cfg config.cfg`

- [x] Entrainement.
  > COMMANDE

`python3 -m spacy train ./config-pl/config.cfg --output ./model-pl/spacy_model2/ --paths.train ./corpus_polonais/corpus-ent/pl_pdb-ud-train.spacy --paths.dev ./corpus_polonais/corpus-ent/pl_pdb-ud-dev.spacy `

> RÉSULTATS
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
  0     800       1084.99     11864.38    76.34    0.76
  0    1000       1332.52     13126.04    78.57    0.79
  0    1200       1639.41     14850.34    80.11    0.80
  1    1400       1937.67     16488.74    82.07    0.82
  1    1600       2184.40     16983.03    83.14    0.83
  1    1800       2852.31     20255.85    83.79    0.84
  2    2000       3275.83     21863.38    84.49    0.84
  2    2200       4000.05     23980.72    85.24    0.85
  3    2400       4549.12     25353.81    85.72    0.86
  4    2600       4629.49     23533.87    86.05    0.86
  4    2800       4665.95     21771.22    86.22    0.86
  5    3000       4453.16     19505.36    86.20    0.86
  6    3200       4480.07     18503.58    86.29    0.86
  6    3400       4630.07     17898.17    86.42    0.86
  7    3600       4181.60     15357.95    86.57    0.87
  8    3800       4276.53     15052.16    86.57    0.87
  9    4000       4443.97     14838.22    86.61    0.87
  9    4200       4180.28     13335.14    86.78    0.87
 10    4400       4024.20     12438.06    86.96    0.87
 11    4600       4145.21     12311.66    86.84    0.87
 11    4800       4194.93     12028.49    86.97    0.87
 12    5000       3836.28     10688.01    86.92    0.87
 13    5200       3961.42     10696.97    86.99    0.87
 14    5400       4073.70     10637.41    86.96    0.87
 14    5600       3859.94      9812.63    87.00    0.87
 15    5800       3763.06      9331.90    87.11    0.87
 16    6000       3897.93      9442.78    87.02    0.87
 16    6200       3817.87      9016.81    87.02    0.87
 17    6400       3607.09      8348.69    87.05    0.87
 18    6600       3728.61      8420.33    87.12    0.87
 18    6800       3869.41      8519.29    87.27    0.87
 19    7000       3531.77      7607.39    87.23    0.87
 20    7200       3573.85      7570.14    87.34    0.87
 21    7400       3767.19      7835.26    87.25    0.87
 21    7600       3580.09      7300.13    87.30    0.87
 22    7800       3532.65      7043.71    87.33    0.87
 23    8000       3624.37      7113.76    87.21    0.87
 23    8200       3645.53      7033.19    87.35    0.87
 24    8400       3395.14      6425.91    87.29    0.87
 25    8600       3501.54      6516.88    87.33    0.87
 26    8800       3595.23      6592.79    87.38    0.87
 26    9000       3361.76      6070.03    87.12    0.87
 27    9200       3404.39      6039.19    87.26    0.87
 28    9400       3418.34      5959.09    87.30    0.87
 28    9600       3463.41      5952.33    87.24    0.87
 29    9800       3329.74      5629.46    87.28    0.87
 30   10000       3447.69      5749.63    87.42    0.87
 31   10200       3493.28      5727.72    87.29    0.87
 31   10400       3295.58      5324.52    87.36    0.87
 32   10600       3360.99      5355.66    87.30    0.87
 33   10800       3405.74      5369.69    87.38    0.87
 33   11000       3361.57      5249.01    87.50    0.88
 34   11200       3280.03      5029.87    87.41    0.87
 35   11400       3402.37      5124.84    87.49    0.87
 35   11600       3482.64      5183.55    87.33    0.87
 36   11800       3218.74      4735.76    87.38    0.87
 37   12000       3436.31      4986.79    87.50    0.87
 38   12200       3499.44      5040.71    87.47    0.87
 38   12400       3266.91      4654.40    87.41    0.87
 39   12600       3288.62      4601.40    87.38    0.87
```

- [x] Évaluation.
  > COMMANDE
  > `python3 scripts/eval-polonais.py`

> RÉSULTATS

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
                adj:pl:acc:f:pos       0.00      0.00      0.00      60.0
                adj:pl:acc:f:sup       0.00      0.00      0.00       1.0
               adj:pl:acc:m1:pos       0.00      0.00      0.00      15.0
               adj:pl:acc:m2:pos       0.00      0.00      0.00       1.0
               adj:pl:acc:m3:pos       0.00      0.00      0.00      81.0
               adj:pl:acc:m3:sup       0.00      0.00      0.00       1.0
                adj:pl:acc:n:com       0.00      0.00      0.00       1.0
                adj:pl:acc:n:pos       0.00      0.00      0.00      27.0
                adj:pl:dat:f:pos       0.00      0.00      0.00       3.0
               adj:pl:dat:m1:pos       0.00      0.00      0.00       5.0
               adj:pl:dat:m3:pos       0.00      0.00      0.00       2.0
                adj:pl:dat:n:pos       0.00      0.00      0.00       4.0
                adj:pl:gen:f:com       0.00      0.00      0.00       2.0
                adj:pl:gen:f:pos       0.00      0.00      0.00     127.0
                adj:pl:gen:f:sup       0.00      0.00      0.00       1.0
               adj:pl:gen:m1:pos       0.00      0.00      0.00      45.0
               adj:pl:gen:m1:sup       0.00      0.00      0.00       2.0
               adj:pl:gen:m3:com       0.00      0.00      0.00       1.0
               adj:pl:gen:m3:pos       0.00      0.00      0.00     114.0
               adj:pl:gen:m3:sup       0.00      0.00      0.00       1.0
                adj:pl:gen:n:pos       0.00      0.00      0.00      71.0
               adj:pl:inst:f:com       0.00      0.00      0.00       1.0
               adj:pl:inst:f:pos       0.00      0.00      0.00      21.0
              adj:pl:inst:m1:pos       0.00      0.00      0.00       5.0
              adj:pl:inst:m3:pos       0.00      0.00      0.00      30.0
               adj:pl:inst:n:pos       0.00      0.00      0.00      15.0
                adj:pl:loc:f:pos       0.00      0.00      0.00      43.0
               adj:pl:loc:m3:pos       0.00      0.00      0.00      44.0
               adj:pl:loc:m3:sup       0.00      0.00      0.00       1.0
                adj:pl:loc:n:com       0.00      0.00      0.00       1.0
                adj:pl:loc:n:pos       0.00      0.00      0.00      37.0
                adj:pl:nom:f:com       0.00      0.00      0.00       1.0
                adj:pl:nom:f:pos       0.00      0.00      0.00      83.0
               adj:pl:nom:m1:pos       0.00      0.00      0.00      75.0
               adj:pl:nom:m2:pos       0.00      0.00      0.00       2.0
               adj:pl:nom:m3:com       0.00      0.00      0.00       1.0
               adj:pl:nom:m3:pos       0.00      0.00      0.00      79.0
               adj:pl:nom:m3:sup       0.00      0.00      0.00       1.0
                adj:pl:nom:n:pos       0.00      0.00      0.00      29.0
                adj:sg:acc:f:com       0.00      0.00      0.00       5.0
                adj:sg:acc:f:pos       0.00      0.00      0.00     185.0
                adj:sg:acc:f:sup       0.00      0.00      0.00       1.0
               adj:sg:acc:m1:pos       0.00      0.00      0.00      15.0
               adj:sg:acc:m2:pos       0.00      0.00      0.00       1.0
               adj:sg:acc:m3:com       0.00      0.00      0.00       4.0
               adj:sg:acc:m3:pos       0.00      0.00      0.00     180.0
                adj:sg:acc:n:pos       0.00      0.00      0.00      88.0
                adj:sg:acc:n:sup       0.00      0.00      0.00       1.0
                adj:sg:dat:f:pos       0.00      0.00      0.00       4.0
               adj:sg:dat:m1:pos       0.00      0.00      0.00       4.0
               adj:sg:dat:m3:pos       0.00      0.00      0.00       3.0
                adj:sg:dat:n:pos       0.00      0.00      0.00       1.0
                adj:sg:gen:f:com       0.00      0.00      0.00       1.0
                adj:sg:gen:f:pos       0.00      0.00      0.00     305.0
                adj:sg:gen:f:sup       0.00      0.00      0.00       1.0
               adj:sg:gen:m1:pos       0.00      0.00      0.00      28.0
               adj:sg:gen:m2:pos       0.00      0.00      0.00       6.0
               adj:sg:gen:m3:com       0.00      0.00      0.00       3.0
               adj:sg:gen:m3:pos       0.00      0.00      0.00     211.0
                adj:sg:gen:n:com       0.00      0.00      0.00       2.0
                adj:sg:gen:n:pos       0.00      0.00      0.00     122.0
                adj:sg:gen:n:sup       0.00      0.00      0.00       1.0
               adj:sg:inst:f:com       0.00      0.00      0.00       1.0
               adj:sg:inst:f:pos       0.00      0.00      0.00      63.0
               adj:sg:inst:f:sup       0.00      0.00      0.00       4.0
              adj:sg:inst:m1:pos       0.00      0.00      0.00      18.0
              adj:sg:inst:m1:sup       0.00      0.00      0.00       2.0
              adj:sg:inst:m3:com       0.00      0.00      0.00       1.0
              adj:sg:inst:m3:pos       0.00      0.00      0.00      89.0
              adj:sg:inst:m3:sup       0.00      0.00      0.00       2.0
               adj:sg:inst:n:pos       0.00      0.00      0.00      37.0
                adj:sg:loc:f:com       0.00      0.00      0.00       1.0
                adj:sg:loc:f:pos       0.00      0.00      0.00     127.0
               adj:sg:loc:m2:pos       0.00      0.00      0.00       2.0
               adj:sg:loc:m3:com       0.00      0.00      0.00       3.0
               adj:sg:loc:m3:pos       0.00      0.00      0.00     188.0
                adj:sg:loc:n:pos       0.00      0.00      0.00      43.0
                adj:sg:loc:n:sup       0.00      0.00      0.00       1.0
                adj:sg:nom:f:com       0.00      0.00      0.00      11.0
                adj:sg:nom:f:pos       0.00      0.00      0.00     251.0
                adj:sg:nom:f:sup       0.00      0.00      0.00       2.0
               adj:sg:nom:m1:com       0.00      0.00      0.00       3.0
               adj:sg:nom:m1:pos       0.00      0.00      0.00     156.0
               adj:sg:nom:m2:pos       0.00      0.00      0.00      23.0
               adj:sg:nom:m3:pos       0.00      0.00      0.00     177.0
               adj:sg:nom:m3:sup       0.00      0.00      0.00       2.0
                adj:sg:nom:n:com       0.00      0.00      0.00       3.0
                adj:sg:nom:n:pos       0.00      0.00      0.00     111.0
                adj:sg:nom:n:sup       0.00      0.00      0.00       4.0
                            adja       0.00      0.00      0.00      22.0
                            adjc       0.00      0.00      0.00       2.0
                        adjp:dat       0.00      0.00      0.00       9.0
                        adjp:gen       0.00      0.00      0.00       2.0
                             adv       0.00      0.00      0.00     492.0
                         adv:com       0.00      0.00      0.00      74.0
                         adv:pos       0.00      0.00      0.00     508.0
                         adv:sup       0.00      0.00      0.00      18.0
            bedzie:pl:pri:imperf       0.00      0.00      0.00      11.0
            bedzie:pl:ter:imperf       0.00      0.00      0.00      27.0
            bedzie:sg:pri:imperf       0.00      0.00      0.00       4.0
            bedzie:sg:sec:imperf       0.00      0.00      0.00       4.0
            bedzie:sg:ter:imperf       0.00      0.00      0.00      62.0
                       brev:npun       0.00      0.00      0.00     131.0
                        brev:pun       0.00      0.00      0.00     141.0
                            comp       0.00      0.00      0.00     702.0
                            conj       0.00      0.00      0.00    1048.0
                             dig       0.00      0.00      0.00      96.0
               fin:pl:pri:imperf       0.00      0.00      0.00      95.0
                 fin:pl:pri:perf       0.00      0.00      0.00       8.0
               fin:pl:sec:imperf       0.00      0.00      0.00       7.0
                 fin:pl:sec:perf       0.00      0.00      0.00       2.0
               fin:pl:ter:imperf       0.00      0.00      0.00     365.0
                 fin:pl:ter:perf       0.00      0.00      0.00      25.0
               fin:sg:pri:imperf       0.00      0.00      0.00     195.0
                 fin:sg:pri:perf       0.00      0.00      0.00      23.0
               fin:sg:sec:imperf       0.00      0.00      0.00      50.0
                 fin:sg:sec:perf       0.00      0.00      0.00      11.0
               fin:sg:ter:imperf       0.00      0.00      0.00    1021.0
                 fin:sg:ter:perf       0.00      0.00      0.00      73.0
                            frag       0.00      0.00      0.00       9.0
         ger:pl:nom:n:imperf:aff       0.00      0.00      0.00       1.0
         ger:sg:acc:n:imperf:aff       0.00      0.00      0.00      19.0
           ger:sg:acc:n:perf:aff       0.00      0.00      0.00      64.0
         ger:sg:dat:n:imperf:aff       0.00      0.00      0.00       2.0
           ger:sg:dat:n:perf:aff       0.00      0.00      0.00       1.0
         ger:sg:gen:n:imperf:aff       0.00      0.00      0.00      98.0
           ger:sg:gen:n:perf:aff       0.00      0.00      0.00      94.0
        ger:sg:inst:n:imperf:aff       0.00      0.00      0.00      10.0
          ger:sg:inst:n:perf:aff       0.00      0.00      0.00      11.0
         ger:sg:loc:n:imperf:aff       0.00      0.00      0.00      16.0
           ger:sg:loc:n:perf:aff       0.00      0.00      0.00      26.0
         ger:sg:nom:n:imperf:aff       0.00      0.00      0.00      24.0
           ger:sg:nom:n:perf:aff       0.00      0.00      0.00      23.0
                             ign       0.00      0.00      0.00       9.0
                     imps:imperf       0.00      0.00      0.00       6.0
                       imps:perf       0.00      0.00      0.00      62.0
              impt:pl:pri:imperf       0.00      0.00      0.00       2.0
                impt:pl:pri:perf       0.00      0.00      0.00       6.0
              impt:pl:sec:imperf       0.00      0.00      0.00       1.0
              impt:sg:sec:imperf       0.00      0.00      0.00      15.0
                impt:sg:sec:perf       0.00      0.00      0.00      38.0
                      inf:imperf       0.00      0.00      0.00     257.0
                        inf:perf       0.00      0.00      0.00     332.0
                          interj       0.00      0.00      0.00      15.0
                          interp       0.00      0.00      0.00    5631.0
         num:pl:acc:f:congr:ncol       0.00      0.00      0.00       8.0
                num:pl:acc:f:rec       0.00      0.00      0.00      10.0
           num:pl:acc:f:rec:ncol       0.00      0.00      0.00       4.0
               num:pl:acc:m1:rec       0.00      0.00      0.00       1.0
          num:pl:acc:m1:rec:ncol       0.00      0.00      0.00       2.0
               num:pl:acc:m2:rec       0.00      0.00      0.00       7.0
        num:pl:acc:m3:congr:ncol       0.00      0.00      0.00      16.0
               num:pl:acc:m3:rec       0.00      0.00      0.00      46.0
          num:pl:acc:m3:rec:ncol       0.00      0.00      0.00      21.0
           num:pl:acc:n:rec:ncol       0.00      0.00      0.00       6.0
         num:pl:dat:f:congr:ncol       0.00      0.00      0.00       1.0
             num:pl:dat:m1:congr       0.00      0.00      0.00       1.0
              num:pl:gen:f:congr       0.00      0.00      0.00       6.0
         num:pl:gen:f:congr:ncol       0.00      0.00      0.00       6.0
             num:pl:gen:m1:congr       0.00      0.00      0.00       4.0
        num:pl:gen:m1:congr:ncol       0.00      0.00      0.00       4.0
             num:pl:gen:m2:congr       0.00      0.00      0.00       1.0
             num:pl:gen:m3:congr       0.00      0.00      0.00      27.0
        num:pl:gen:m3:congr:ncol       0.00      0.00      0.00      13.0
              num:pl:gen:n:congr       0.00      0.00      0.00       2.0
         num:pl:gen:n:congr:ncol       0.00      0.00      0.00       4.0
        num:pl:inst:f:congr:ncol       0.00      0.00      0.00       3.0
       num:pl:inst:m3:congr:ncol       0.00      0.00      0.00       2.0
              num:pl:loc:f:congr       0.00      0.00      0.00       1.0
         num:pl:loc:f:congr:ncol       0.00      0.00      0.00       9.0
             num:pl:loc:m3:congr       0.00      0.00      0.00       4.0
        num:pl:loc:m3:congr:ncol       0.00      0.00      0.00       3.0
         num:pl:loc:n:congr:ncol       0.00      0.00      0.00       1.0
         num:pl:nom:f:congr:ncol       0.00      0.00      0.00      22.0
                num:pl:nom:f:rec       0.00      0.00      0.00       8.0
           num:pl:nom:f:rec:ncol       0.00      0.00      0.00       9.0
        num:pl:nom:m1:congr:ncol       0.00      0.00      0.00       4.0
               num:pl:nom:m1:rec       0.00      0.00      0.00       9.0
           num:pl:nom:m1:rec:col       0.00      0.00      0.00       2.0
          num:pl:nom:m1:rec:ncol       0.00      0.00      0.00      17.0
        num:pl:nom:m2:congr:ncol       0.00      0.00      0.00       3.0
        num:pl:nom:m3:congr:ncol       0.00      0.00      0.00       5.0
               num:pl:nom:m3:rec       0.00      0.00      0.00      23.0
          num:pl:nom:m3:rec:ncol       0.00      0.00      0.00       2.0
         num:pl:nom:n:congr:ncol       0.00      0.00      0.00       3.0
                num:pl:nom:n:rec       0.00      0.00      0.00       1.0
            num:pl:nom:n:rec:col       0.00      0.00      0.00       3.0
           num:pl:nom:n:rec:ncol       0.00      0.00      0.00       2.0
                num:sg:acc:f:rec       0.00      0.00      0.00       1.0
               num:sg:acc:m3:rec       0.00      0.00      0.00       3.0
                num:sg:acc:n:rec       0.00      0.00      0.00       1.0
               num:sg:nom:m3:rec       0.00      0.00      0.00       1.0
        pact:pl:acc:f:imperf:aff       0.00      0.00      0.00       6.0
       pact:pl:acc:m1:imperf:aff       0.00      0.00      0.00       2.0
       pact:pl:acc:m3:imperf:aff       0.00      0.00      0.00       3.0
        pact:pl:acc:n:imperf:aff       0.00      0.00      0.00       1.0
        pact:pl:dat:f:imperf:aff       0.00      0.00      0.00       1.0
        pact:pl:gen:f:imperf:aff       0.00      0.00      0.00      10.0
       pact:pl:gen:m1:imperf:aff       0.00      0.00      0.00      14.0
       pact:pl:gen:m3:imperf:aff       0.00      0.00      0.00       6.0
        pact:pl:gen:n:imperf:aff       0.00      0.00      0.00       4.0
       pact:pl:inst:f:imperf:aff       0.00      0.00      0.00       2.0
      pact:pl:inst:m1:imperf:aff       0.00      0.00      0.00       3.0
      pact:pl:inst:m3:imperf:aff       0.00      0.00      0.00       1.0
        pact:pl:loc:f:imperf:aff       0.00      0.00      0.00       1.0
        pact:pl:loc:n:imperf:aff       0.00      0.00      0.00       2.0
        pact:pl:nom:f:imperf:aff       0.00      0.00      0.00       4.0
       pact:pl:nom:m1:imperf:aff       0.00      0.00      0.00       3.0
       pact:pl:nom:m2:imperf:aff       0.00      0.00      0.00       1.0
       pact:pl:nom:m3:imperf:aff       0.00      0.00      0.00       3.0
        pact:pl:nom:n:imperf:aff       0.00      0.00      0.00       1.0
        pact:sg:acc:f:imperf:aff       0.00      0.00      0.00       6.0
       pact:sg:acc:m3:imperf:aff       0.00      0.00      0.00       9.0
        pact:sg:acc:n:imperf:aff       0.00      0.00      0.00       2.0
        pact:sg:gen:f:imperf:aff       0.00      0.00      0.00      17.0
       pact:sg:gen:m1:imperf:aff       0.00      0.00      0.00       2.0
       pact:sg:gen:m2:imperf:aff       0.00      0.00      0.00       1.0
       pact:sg:gen:m3:imperf:aff       0.00      0.00      0.00       4.0
        pact:sg:gen:n:imperf:aff       0.00      0.00      0.00       1.0
       pact:sg:inst:f:imperf:aff       0.00      0.00      0.00       6.0
      pact:sg:inst:m3:imperf:aff       0.00      0.00      0.00       6.0
       pact:sg:inst:n:imperf:aff       0.00      0.00      0.00       5.0
        pact:sg:loc:f:imperf:aff       0.00      0.00      0.00       3.0
       pact:sg:loc:m3:imperf:aff       0.00      0.00      0.00       4.0
        pact:sg:nom:f:imperf:aff       0.00      0.00      0.00      15.0
       pact:sg:nom:m1:imperf:aff       0.00      0.00      0.00      14.0
       pact:sg:nom:m3:imperf:aff       0.00      0.00      0.00       5.0
        pact:sg:nom:n:imperf:aff       0.00      0.00      0.00       5.0
                       pant:perf       0.00      0.00      0.00       4.0
                            part       0.00      0.00      0.00    1672.0
                     pcon:imperf       0.00      0.00      0.00     105.0
          ppas:pl:acc:f:perf:aff       0.00      0.00      0.00       7.0
         ppas:pl:acc:m3:perf:aff       0.00      0.00      0.00       9.0
          ppas:pl:acc:n:perf:aff       0.00      0.00      0.00       4.0
        ppas:pl:gen:f:imperf:aff       0.00      0.00      0.00       2.0
          ppas:pl:gen:f:perf:aff       0.00      0.00      0.00      14.0
         ppas:pl:gen:m1:perf:aff       0.00      0.00      0.00       1.0
       ppas:pl:gen:m3:imperf:aff       0.00      0.00      0.00       4.0
         ppas:pl:gen:m3:perf:aff       0.00      0.00      0.00       5.0
          ppas:pl:gen:n:perf:aff       0.00      0.00      0.00       8.0
         ppas:pl:inst:f:perf:aff       0.00      0.00      0.00       8.0
        ppas:pl:inst:m3:perf:aff       0.00      0.00      0.00       3.0
         ppas:pl:inst:n:perf:aff       0.00      0.00      0.00       3.0
          ppas:pl:loc:f:perf:aff       0.00      0.00      0.00       2.0
       ppas:pl:loc:m3:imperf:aff       0.00      0.00      0.00       1.0
         ppas:pl:loc:m3:perf:aff       0.00      0.00      0.00       1.0
          ppas:pl:loc:n:perf:aff       0.00      0.00      0.00       2.0
        ppas:pl:nom:f:imperf:aff       0.00      0.00      0.00       7.0
          ppas:pl:nom:f:perf:aff       0.00      0.00      0.00      17.0
       ppas:pl:nom:m1:imperf:aff       0.00      0.00      0.00       5.0
         ppas:pl:nom:m1:perf:aff       0.00      0.00      0.00      10.0
       ppas:pl:nom:m3:imperf:aff       0.00      0.00      0.00      16.0
         ppas:pl:nom:m3:perf:aff       0.00      0.00      0.00      22.0
        ppas:pl:nom:n:imperf:aff       0.00      0.00      0.00       3.0
          ppas:pl:nom:n:perf:aff       0.00      0.00      0.00      10.0
          ppas:sg:acc:f:perf:aff       0.00      0.00      0.00      10.0
         ppas:sg:acc:m3:perf:aff       0.00      0.00      0.00      16.0
          ppas:sg:acc:n:perf:aff       0.00      0.00      0.00       3.0
        ppas:sg:gen:f:imperf:aff       0.00      0.00      0.00       2.0
          ppas:sg:gen:f:perf:aff       0.00      0.00      0.00       5.0
         ppas:sg:gen:m1:perf:aff       0.00      0.00      0.00       1.0
         ppas:sg:gen:m3:perf:aff       0.00      0.00      0.00       4.0
          ppas:sg:gen:n:perf:aff       0.00      0.00      0.00       1.0
         ppas:sg:inst:f:perf:aff       0.00      0.00      0.00       6.0
        ppas:sg:inst:m1:perf:aff       0.00      0.00      0.00       1.0
        ppas:sg:inst:m3:perf:aff       0.00      0.00      0.00       8.0
       ppas:sg:inst:n:imperf:aff       0.00      0.00      0.00       1.0
         ppas:sg:inst:n:perf:aff       0.00      0.00      0.00       2.0
          ppas:sg:loc:f:perf:aff       0.00      0.00      0.00       4.0
         ppas:sg:loc:m3:perf:aff       0.00      0.00      0.00       7.0
          ppas:sg:loc:n:perf:aff       0.00      0.00      0.00       2.0
        ppas:sg:nom:f:imperf:aff       0.00      0.00      0.00      16.0
          ppas:sg:nom:f:perf:aff       0.00      0.00      0.00      46.0
       ppas:sg:nom:m1:imperf:aff       0.00      0.00      0.00      10.0
         ppas:sg:nom:m1:perf:aff       0.00      0.00      0.00      14.0
         ppas:sg:nom:m2:perf:aff       0.00      0.00      0.00       2.0
       ppas:sg:nom:m3:imperf:aff       0.00      0.00      0.00       4.0
         ppas:sg:nom:m3:perf:aff       0.00      0.00      0.00      27.0
        ppas:sg:nom:n:imperf:aff       0.00      0.00      0.00       8.0
          ppas:sg:nom:n:perf:aff       0.00      0.00      0.00      28.0
           ppron12:pl:acc:m1:pri       0.00      0.00      0.00      10.0
           ppron12:pl:dat:m1:pri       0.00      0.00      0.00      21.0
           ppron12:pl:gen:m1:pri       0.00      0.00      0.00       1.0
           ppron12:pl:gen:m1:sec       0.00      0.00      0.00       1.0
          ppron12:pl:inst:m1:pri       0.00      0.00      0.00       2.0
           ppron12:pl:nom:m1:pri       0.00      0.00      0.00       8.0
           ppron12:pl:nom:m1:sec       0.00      0.00      0.00       1.0
        ppron12:sg:acc:f:pri:akc       0.00      0.00      0.00       3.0
       ppron12:sg:acc:m1:pri:akc       0.00      0.00      0.00      27.0
       ppron12:sg:acc:m1:sec:akc       0.00      0.00      0.00       4.0
      ppron12:sg:acc:m1:sec:nakc       0.00      0.00      0.00      11.0
       ppron12:sg:dat:f:pri:nakc       0.00      0.00      0.00       3.0
      ppron12:sg:dat:m1:pri:nakc       0.00      0.00      0.00      34.0
      ppron12:sg:dat:m1:sec:nakc       0.00      0.00      0.00      10.0
       ppron12:sg:gen:m1:pri:akc       0.00      0.00      0.00      11.0
       ppron12:sg:gen:m1:sec:akc       0.00      0.00      0.00       3.0
           ppron12:sg:inst:f:sec       0.00      0.00      0.00       1.0
          ppron12:sg:inst:m1:pri       0.00      0.00      0.00       2.0
          ppron12:sg:inst:m1:sec       0.00      0.00      0.00       1.0
           ppron12:sg:loc:m1:pri       0.00      0.00      0.00       2.0
            ppron12:sg:nom:f:pri       0.00      0.00      0.00       1.0
           ppron12:sg:nom:m1:pri       0.00      0.00      0.00      19.0
           ppron12:sg:nom:m1:sec       0.00      0.00      0.00       8.0
  ppron3:pl:acc:f:ter:akc:npraep       0.00      0.00      0.00       5.0
 ppron3:pl:acc:m1:ter:akc:npraep       0.00      0.00      0.00       9.0
  ppron3:pl:acc:m1:ter:akc:praep       0.00      0.00      0.00       3.0
 ppron3:pl:acc:m3:ter:akc:npraep       0.00      0.00      0.00      10.0
  ppron3:pl:acc:m3:ter:akc:praep       0.00      0.00      0.00       1.0
  ppron3:pl:acc:n:ter:akc:npraep       0.00      0.00      0.00       5.0
   ppron3:pl:dat:f:ter:akc:praep       0.00      0.00      0.00       1.0
 ppron3:pl:dat:m1:ter:akc:npraep       0.00      0.00      0.00      18.0
  ppron3:pl:gen:f:ter:akc:npraep       0.00      0.00      0.00       8.0
   ppron3:pl:gen:f:ter:akc:praep       0.00      0.00      0.00       3.0
 ppron3:pl:gen:m1:ter:akc:npraep       0.00      0.00      0.00      18.0
  ppron3:pl:gen:m1:ter:akc:praep       0.00      0.00      0.00       9.0
 ppron3:pl:gen:m3:ter:akc:npraep       0.00      0.00      0.00       8.0
  ppron3:pl:gen:m3:ter:akc:praep       0.00      0.00      0.00       1.0
  ppron3:pl:gen:n:ter:akc:npraep       0.00      0.00      0.00       5.0
   ppron3:pl:gen:n:ter:akc:praep       0.00      0.00      0.00       1.0
 ppron3:pl:inst:m1:ter:akc:praep       0.00      0.00      0.00       6.0
   ppron3:pl:loc:f:ter:akc:praep       0.00      0.00      0.00       1.0
  ppron3:pl:loc:m3:ter:akc:praep       0.00      0.00      0.00       2.0
 ppron3:pl:nom:m1:ter:akc:npraep       0.00      0.00      0.00       3.0
 ppron3:pl:nom:m3:ter:akc:npraep       0.00      0.00      0.00       2.0
  ppron3:pl:nom:n:ter:akc:npraep       0.00      0.00      0.00       1.0
  ppron3:sg:acc:f:ter:akc:npraep       0.00      0.00      0.00      23.0
   ppron3:sg:acc:f:ter:akc:praep       0.00      0.00      0.00       1.0
  ppron3:sg:acc:m1:ter:akc:praep       0.00      0.00      0.00       3.0
ppron3:sg:acc:m1:ter:nakc:npraep       0.00      0.00      0.00      31.0
ppron3:sg:acc:m3:ter:nakc:npraep       0.00      0.00      0.00      10.0
  ppron3:sg:acc:n:ter:akc:npraep       0.00      0.00      0.00       1.0
  ppron3:sg:dat:f:ter:akc:npraep       0.00      0.00      0.00       7.0
ppron3:sg:dat:m1:ter:nakc:npraep       0.00      0.00      0.00      39.0
  ppron3:sg:gen:f:ter:akc:npraep       0.00      0.00      0.00      39.0
   ppron3:sg:gen:f:ter:akc:praep       0.00      0.00      0.00       7.0
 ppron3:sg:gen:m1:ter:akc:npraep       0.00      0.00      0.00      48.0
  ppron3:sg:gen:m1:ter:akc:praep       0.00      0.00      0.00       8.0
ppron3:sg:gen:m1:ter:nakc:npraep       0.00      0.00      0.00       3.0
 ppron3:sg:gen:m3:ter:akc:npraep       0.00      0.00      0.00       8.0
  ppron3:sg:inst:f:ter:akc:praep       0.00      0.00      0.00      10.0
ppron3:sg:inst:m1:ter:akc:npraep       0.00      0.00      0.00       1.0
 ppron3:sg:inst:m1:ter:akc:praep       0.00      0.00      0.00      12.0
   ppron3:sg:loc:f:ter:akc:praep       0.00      0.00      0.00       4.0
  ppron3:sg:loc:m1:ter:akc:praep       0.00      0.00      0.00       1.0
  ppron3:sg:loc:m3:ter:akc:praep       0.00      0.00      0.00       3.0
   ppron3:sg:loc:n:ter:akc:praep       0.00      0.00      0.00       2.0
  ppron3:sg:nom:f:ter:akc:npraep       0.00      0.00      0.00      12.0
 ppron3:sg:nom:m1:ter:akc:npraep       0.00      0.00      0.00      15.0
  ppron3:sg:nom:n:ter:akc:npraep       0.00      0.00      0.00       3.0
               praet:pl:f:imperf       0.00      0.00      0.00      27.0
                 praet:pl:f:perf       0.00      0.00      0.00      24.0
              praet:pl:m1:imperf       0.00      0.00      0.00      97.0
                praet:pl:m1:perf       0.00      0.00      0.00      82.0
              praet:pl:m2:imperf       0.00      0.00      0.00       2.0
              praet:pl:m3:imperf       0.00      0.00      0.00      11.0
                praet:pl:m3:perf       0.00      0.00      0.00      23.0
               praet:pl:n:imperf       0.00      0.00      0.00      11.0
                 praet:pl:n:perf       0.00      0.00      0.00       8.0
               praet:sg:f:imperf       0.00      0.00      0.00     132.0
                 praet:sg:f:perf       0.00      0.00      0.00     203.0
              praet:sg:m1:imperf       0.00      0.00      0.00     223.0
         praet:sg:m1:imperf:nagl       0.00      0.00      0.00       7.0
                praet:sg:m1:perf       0.00      0.00      0.00     353.0
           praet:sg:m1:perf:nagl       0.00      0.00      0.00       5.0
              praet:sg:m2:imperf       0.00      0.00      0.00       1.0
                praet:sg:m2:perf       0.00      0.00      0.00       3.0
              praet:sg:m3:imperf       0.00      0.00      0.00      40.0
                praet:sg:m3:perf       0.00      0.00      0.00      52.0
               praet:sg:n:imperf       0.00      0.00      0.00      90.0
                 praet:sg:n:perf       0.00      0.00      0.00      80.0
                            pred       0.00      0.00      0.00     151.0
                        prep:acc       0.00      0.00      0.00     482.0
                   prep:acc:nwok       0.00      0.00      0.00     213.0
                    prep:acc:wok       0.00      0.00      0.00       2.0
                        prep:dat       0.00      0.00      0.00      29.0
                        prep:gen       0.00      0.00      0.00     550.0
                   prep:gen:nwok       0.00      0.00      0.00     345.0
                    prep:gen:wok       0.00      0.00      0.00      25.0
                       prep:inst       0.00      0.00      0.00      55.0
                  prep:inst:nwok       0.00      0.00      0.00     358.0
                   prep:inst:wok       0.00      0.00      0.00      35.0
                        prep:loc       0.00      0.00      0.00     585.0
                   prep:loc:nwok       0.00      0.00      0.00     831.0
                    prep:loc:wok       0.00      0.00      0.00      18.0
                      siebie:acc       0.00      0.00      0.00       6.0
                      siebie:dat       0.00      0.00      0.00      22.0
                      siebie:gen       0.00      0.00      0.00      12.0
                     siebie:inst       0.00      0.00      0.00      10.0
                      siebie:loc       0.00      0.00      0.00       4.0
                  subst:pl:acc:f       0.00      0.00      0.00     129.0
                 subst:pl:acc:m1       0.00      0.00      0.00      31.0
                 subst:pl:acc:m2       0.00      0.00      0.00       5.0
                 subst:pl:acc:m3       0.00      0.00      0.00     169.0
              subst:pl:acc:n:col       0.00      0.00      0.00       6.0
             subst:pl:acc:n:ncol       0.00      0.00      0.00      42.0
               subst:pl:acc:n:pt       0.00      0.00      0.00      30.0
                  subst:pl:dat:f       0.00      0.00      0.00       7.0
                 subst:pl:dat:m1       0.00      0.00      0.00      36.0
                 subst:pl:dat:m3       0.00      0.00      0.00       1.0
             subst:pl:dat:n:ncol       0.00      0.00      0.00       3.0
                  subst:pl:gen:f       0.00      0.00      0.00     265.0
                 subst:pl:gen:m1       0.00      0.00      0.00     186.0
              subst:pl:gen:m1:pt       0.00      0.00      0.00       7.0
                 subst:pl:gen:m2       0.00      0.00      0.00      18.0
                 subst:pl:gen:m3       0.00      0.00      0.00     284.0
              subst:pl:gen:n:col       0.00      0.00      0.00      18.0
             subst:pl:gen:n:ncol       0.00      0.00      0.00     113.0
               subst:pl:gen:n:pt       0.00      0.00      0.00      40.0
                 subst:pl:inst:f       0.00      0.00      0.00      57.0
                subst:pl:inst:m1       0.00      0.00      0.00      18.0
                subst:pl:inst:m2       0.00      0.00      0.00       1.0
                subst:pl:inst:m3       0.00      0.00      0.00      61.0
             subst:pl:inst:n:col       0.00      0.00      0.00       1.0
            subst:pl:inst:n:ncol       0.00      0.00      0.00      17.0
              subst:pl:inst:n:pt       0.00      0.00      0.00       7.0
                  subst:pl:loc:f       0.00      0.00      0.00     100.0
                 subst:pl:loc:m1       0.00      0.00      0.00       1.0
                 subst:pl:loc:m3       0.00      0.00      0.00      98.0
              subst:pl:loc:n:col       0.00      0.00      0.00       2.0
             subst:pl:loc:n:ncol       0.00      0.00      0.00      26.0
               subst:pl:loc:n:pt       0.00      0.00      0.00      47.0
                  subst:pl:nom:f       0.00      0.00      0.00     146.0
                 subst:pl:nom:m1       0.00      0.00      0.00     141.0
              subst:pl:nom:m1:pt       0.00      0.00      0.00       9.0
                 subst:pl:nom:m2       0.00      0.00      0.00      10.0
                 subst:pl:nom:m3       0.00      0.00      0.00      97.0
              subst:pl:nom:n:col       0.00      0.00      0.00       5.0
             subst:pl:nom:n:ncol       0.00      0.00      0.00      39.0
               subst:pl:nom:n:pt       0.00      0.00      0.00      29.0
                  subst:sg:acc:f       0.00      0.00      0.00     464.0
                 subst:sg:acc:m1       0.00      0.00      0.00      73.0
                 subst:sg:acc:m2       0.00      0.00      0.00       6.0
                 subst:sg:acc:m3       0.00      0.00      0.00     461.0
              subst:sg:acc:n:col       0.00      0.00      0.00       4.0
             subst:sg:acc:n:ncol       0.00      0.00      0.00     257.0
                  subst:sg:dat:f       0.00      0.00      0.00      32.0
                 subst:sg:dat:m1       0.00      0.00      0.00      28.0
                 subst:sg:dat:m3       0.00      0.00      0.00      12.0
             subst:sg:dat:n:ncol       0.00      0.00      0.00       4.0
                  subst:sg:gen:f       0.00      0.00      0.00     913.0
                 subst:sg:gen:m1       0.00      0.00      0.00     227.0
                 subst:sg:gen:m2       0.00      0.00      0.00      17.0
                 subst:sg:gen:m3       0.00      0.00      0.00     647.0
              subst:sg:gen:n:col       0.00      0.00      0.00       3.0
             subst:sg:gen:n:ncol       0.00      0.00      0.00     340.0
                 subst:sg:inst:f       0.00      0.00      0.00     225.0
                subst:sg:inst:m1       0.00      0.00      0.00      50.0
                subst:sg:inst:m3       0.00      0.00      0.00     322.0
             subst:sg:inst:n:col       0.00      0.00      0.00       5.0
            subst:sg:inst:n:ncol       0.00      0.00      0.00      96.0
                  subst:sg:loc:f       0.00      0.00      0.00     446.0
                 subst:sg:loc:m2       0.00      0.00      0.00       3.0
                 subst:sg:loc:m3       0.00      0.00      0.00     487.0
              subst:sg:loc:n:col       0.00      0.00      0.00       1.0
             subst:sg:loc:n:ncol       0.00      0.00      0.00     157.0
                  subst:sg:nom:f       0.00      0.00      0.00     615.0
                 subst:sg:nom:m1       0.00      0.00      0.00     671.0
                 subst:sg:nom:m2       0.00      0.00      0.00      37.0
                 subst:sg:nom:m3       0.00      0.00      0.00     335.0
              subst:sg:nom:n:col       0.00      0.00      0.00      20.0
             subst:sg:nom:n:ncol       0.00      0.00      0.00     284.0
                  subst:sg:voc:f       0.00      0.00      0.00       3.0
                 subst:sg:voc:m1       0.00      0.00      0.00      21.0
             subst:sg:voc:n:ncol       0.00      0.00      0.00       1.0
                             sym       0.00      0.00      0.00       2.0
             winien:pl:m1:imperf       0.00      0.00      0.00       8.0
             winien:pl:m3:imperf       0.00      0.00      0.00       3.0
              winien:pl:n:imperf       0.00      0.00      0.00       2.0
              winien:sg:f:imperf       0.00      0.00      0.00       7.0
             winien:sg:m1:imperf       0.00      0.00      0.00       7.0
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

# ARABE

- [x] Télécharger le corpus conllu (train, dev et test) pour l'arabe.
- [ ] Convertir le corpus en corpus d'entrainement.
  > COMMANDES :

`python3 -m spacy convert corpus_arabe/corpus-nyuad/ar_nyuad-ud-train.conllu corpus_arabe/corpus-ent`

`python3 -m spacy convert corpus_arabe/corpus-nyuad/ar_nyuad-ud-dev.conllu corpus_arabe/corpus-ent `

`python3 -m spacy convert corpus_arabe/corpus-nyuad/ar_nyuad-ud-test.conllu corpus_arabe/corpus-ent`

- [ ] Configuration de la pipeline.
  > COMMANDE :

`python -m spacy init fill-config config-ar/base_config.cfg config.cfg`

- [ ] Entrainement.
  > COMMANDE :

`python3 -m spacy train ./config-ar/config.cfg --output ./model-ar/spacy_model2/ --paths.train ./corpus_arabe/corpus-ent/ar_nyuad-ud-train.spacy --paths.dev ./corpus_arabe/corpus-ent/ar_nyuad-ud-dev.spacy `

> RÉSULTATS

```

```

- [ ] Évaluation.
  > COMMANDE

`python3 scripts/eval-arabe.py`

> RÉSULTATS

```

```
