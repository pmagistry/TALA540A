# TP - entrainement

## Étape 1 : préparation du corpus

- [x] Télécharger le corpus conllu (train, dev et test).
- [x] Convertir le corpus en corpus d'entrainement.
- [ ] À faire sur d'autres (sous-)corpus.

Commande : `python3 -m spacy corpus/corpus_eval/fr_sequoia-ud-dev.conllu corpus/spacy_sequoia/fr_sequoia-ud-dev.spacy`

## Étape 2 : configuration de la pipeline

- [x] Configurer un modéle pour le français, uniquement un tagger et optimisé vitesse 'efficiency'.
- [x] Télécharger le base_config.cfg.
- [x] Télécharger la commande : `python -m spacy init fill-config base_config.cfg config.cfg`.
- [ ] Modifier base.cfg.

## Étape 3 : entrainement

- [x] Entrainer le modèle sur le corpus d'entrainement.
  > Commande : `python3 -m spacy train config/config.cfg --output ./spacy_model2/ --paths.train corpus/spacy_sequoia/fr_sequoia-ud-train.spacy --paths.dev corpus/spacy_sequoia/fr_sequoia-ud-dev.spacy`

> Résultats :

```
=============== Initializing pipeline =================
✔ Initialized pipeline

================= Training pipeline ===================
ℹ Pipeline: ['tok2vec', 'tagger']
ℹ Initial learn rate: 0.001
E    #       LOSS TOK2VEC  LOSS TAGGER  TAG_ACC  SCORE
---  ------  ------------  -----------  -------  ------
  0       0          0.00        66.37    28.19    0.28
  0     200        139.17      4807.22    89.09    0.89
  0     400        159.31      2288.59    91.80    0.92
  1     600        110.22      1476.40    92.97    0.93
  2     800        103.29      1382.47    93.17    0.93
  3    1000         70.60       934.74    93.55    0.94
  4    1200         49.79       678.43    93.76    0.94
  5    1400         36.73       522.73    93.68    0.94
  7    1600         28.06       425.16    93.68    0.94
  9    1800         19.57       310.50    93.52    0.94
 12    2000         16.63       276.72    93.72    0.94
 15    2200         12.50       218.61    93.73    0.94
 19    2400          9.11       167.11    93.66    0.94
 23    2600          7.28       138.16    93.48    0.93
 27    2800          5.61       109.72    93.63    0.94
```

## Étape 4 : évaluation

- [x] Évaluer le modèle sur le corpus de test.
  > Commande : `python3 eval.py`
  > Résultats :

```
spacy_model2/model-best
annodis
(0.9650872817955112, 0.8636363636363636)
frwiki
(0.9649228908376172, 0.796875)
emea
(0.9791666666666666, 0.8402366863905325)
Europar
(0.9716312056737588, 0.8547008547008547)
fr_core_news_sm
annodis
(0.9613466334164589, 0.8585858585858586)
frwiki
(0.9579679467795585, 0.725)
emea
(0.9769736842105263, 0.7869822485207101)
Europar
(0.9616186900292032, 0.7692307692307693)
fr_core_news_md
annodis
(0.9756857855361596, 0.9393939393939394)
frwiki
(0.9721802237677654, 0.878125)
emea
(0.9788011695906432, 0.8698224852071006)
Europar
(0.9778890279516061, 0.905982905982906)
fr_core_news_lg
annodis
(0.976932668329177, 0.9343434343434344)
frwiki
(0.9745993347444813, 0.890625)
emea
(0.9842836257309941, 0.8816568047337278)
Europar
(0.9787234042553191, 0.9188034188034188)
```

## Étape 5 : refaire la même chose sur d'autres langues

- [ ] Télécharger le corpus conllu (train, dev et test) pour le polonais.
- [ ] Convertir le corpus en corpus d'entrainement.
- [ ] Configuration de la pipeline.
- [ ] Entrainement.
- [ ] Évaluation.
