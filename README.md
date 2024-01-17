TALA540A : TP de Laura Darenne

## environnement de travail

La majorité des modules nécessaires peuvent être téléchargé avec le fichier requirements.

```shell 
$ conda create --name <env> --file requirements.txt
```

### dossier corpus

Le dossier contient tous les corpus pré-traités et les fichiers vecteurs utilisés pour l'entraînement. Il y a également les fichiers python utilisés pour le pré-traitement.

### dossier evaluations

Le dossier contient tous les fichiers python qui ont été utilisé pour évaluer les modèles d'étiquetage en partie du discours. Vous pouvez appelé l'un des trois fichiers suivants : evaluate_jiayan.py, evaluate_spacy.py, evaluate_time.py.

### dossier evaluations_result

Le dossier contient les résultats des évaluations faites avec les fichiers python du dossier evaluations.

### dossier models

Le dossier models contient les fichiers utilisés pour entraîner les modèles. Les modèles n'ont pas été poussé mais ils se trouvent normalement dans les dossiers jiayan et spacy.