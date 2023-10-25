# TP2

### Entraînement du modèle :

J'ai laissé les paramètres par défaut :
* batch_size : 1000
* max_epoch : 0
* max_step : 20000

### Évaluation :

J'ai lancé l'évaluation avec la correction du script eval_basique.py

Pour pouvoir comparer les deux modèles  :
```py
 for model_name in ("fr_core_news_sm", "./model/model-best/"):
```
Sur mon modèle cependant tout est à 0 :

```
accuracy : 0.0, oov : 0.0
              precision    recall  f1-score   support

                   0.00      0.00      0.00   10044.0
         ADJ       0.00      0.00      0.00       0.0
         ADP       0.00      0.00      0.00       0.0
         ADV       0.00      0.00      0.00       0.0
         AUX       0.00      0.00      0.00       0.0
       CCONJ       0.00      0.00      0.00       0.0
         DET       0.00      0.00      0.00       0.0
        NOUN       0.00      0.00      0.00       0.0
         NUM       0.00      0.00      0.00       0.0
        PRON       0.00      0.00      0.00       0.0
       PROPN       0.00      0.00      0.00       0.0
       PUNCT       0.00      0.00      0.00       0.0
       SCONJ       0.00      0.00      0.00       0.0
         SYM       0.00      0.00      0.00       0.0
        VERB       0.00      0.00      0.00       0.0
           X       0.00      0.00      0.00       0.0

    accuracy                           0.00   10044.0
   macro avg       0.00      0.00      0.00   10044.0
weighted avg       0.00      0.00      0.00   10044.0
```
