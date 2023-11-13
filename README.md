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

> RÉSULTATS (j'ai du arrêter l'entrainement car c'était trop long)

```
================ Initializing pipeline ===============
✔ Initialized pipeline

=============== Training pipeline ====================
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
```

- [ ] Évaluation.
  > COMMANDE
  > ` `

> RÉSULTATS

```

```

# ARABE

- [x] Télécharger le corpus conllu (train, dev et test) pour le polonais.
- [ ] Convertir le corpus en corpus d'entrainement.
  > COMMANDES :

`python3 -m spacy convert corpus_arabe/corpus-pdb/ar_nyuad-ud-train.conllu corpus_arabe/corpus-ent`

`python3 -m spacy convert corpus_arabe/corpus-pdb/ar_nyuad-ud-dev.conllu corpus_arabe/corpus-ent `

`python3 -m spacy convert corpus_arabe/corpus-pdb/ar_nyuad-ud-test.conllu corpus_arabe/corpus-ent`

- [ ] Configuration de la pipeline.
  > COMMANDE :

`python -m spacy init fill-config config-ar/base_config.cfg config.cfg`

- [ ] Entrainement.
  > COMMANDE

`python3 -m spacy train ./config-ar/config.cfg --output ./model-ar/spacy_model2/ --paths.train ./corpus_arabe/corpus-ent/ar_nyuad-ud-train.spacy --paths.dev ./corpus_arabe/corpus-ent/ar_nyuad-ud-dev.spacy `

> RÉSULTATS

```

```

- [ ] Évaluation.
  > COMMANDE

`python3 scripts/eval-polonais.py`

> RÉSULTATS

```

```
