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
### Génération des sous corpus et entraînement :
* Modification du script extract_corpus.py pour qu'il génère les 4 sous corpus contenant chacun 3 catégories :
```py
    ids = ["emea", "Europar","frwiki", "annodis"]
    corpus = read_conll("train_spacy/fr_sequoia-ud-dev.conllu", None)
    for i in range(len(ids)) :
        excluded_index = i
        three_cat = ids[:excluded_index] + ids[excluded_index+1:]
        cat_1 = three_cat[0]
        cat_2 = three_cat[1]
        cat_3 = three_cat[2]
        with open(f"train_spacy/3_cat_corpus/3_cat_corpus_{cat_1}_{cat_2}_{cat_3}-dev.conllu", "w") as file:
            sentences = [ sent for sent in corpus.sentences if  re.split(r"\.|_|-",sent.sent_id)[0] in three_cat ]
            for s in sentences:
                file.write(sentence_to_conll(s))
                
                print(sentence_to_conll(s))
```
* Les conll ont bien été générés pour les corpus de dev et train, cependant impossible de les convertir en fichiers binaires pour entrainer un modèles spacy 
```sh
 python -m spacy convert 3_cat_corpus_emea_frwiki_annodis-dev.conllu .
 ### Output :
     id_, word, lemma, pos, tag, morph, head, dep, _1, misc = parts
ValueError: not enough values to unpack (expected 10, got 1)
```
Les Conll générés ne sont sûrement pas au bon format mais je n'ai pas réussi à trouver le problème. 
