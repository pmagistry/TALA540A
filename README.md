# TALA540A : TP de Laura Darenne

## liste des fichiers
- README.md : explications du tp
- TP_eval.md : étapes du tp à faire

#### python
- tp1.py : fichier python principal du projet
- get_corpus.py : fichier python contenant les fonctions appelées par tp1.py pour obtenir les corpus tokenisés
- get_evaluation.py : fichier python contenant les fonctions appelées par tp1.py pour l'évaluation des tokenisations
- datastructures.py : fichier python contenant les dataclasses 

#### corpus
- fr_sequoia-ud-test.conllu : corpus français
- zh_pud-ud-test.conllu : corpus chinois

---

## TP_eval

### étape 1 : ok
- corpus téléchargés : un corpus français et un corpus chinois

### étape 2 : ok
- tokenisation et analyse du texte avec spacy : on obtient une différence de tokenisation par rapport aux fichiers conllu
- tokenization avec le fichier conllu tout en utilisant spacy : marche !

### étape 3 : ok

- exactitude :
    - accuracy ; precision et rappel en fonction des tags
    - rajout des oov

- vitesse
    - bash `time`
    ``` shell
        (project) laura@laura:~/Documents/TALA540A$ time python script/tp1.py
        
        ...
        ...

        real    0m17,677s
        user    0m17,428s
        sys     0m0,879s

    ```
    ```shell
    (project) laura@laura:~/Documents/TALA540A$ time python script/tp1.py -e spacy_retokenize
    conllu: 100%|██████████████████████████████| 456/456 [00:00<00:00, 27609.24it/s]
    spacy_retokenize: 100%|█████████████████████| 456/456 [00:00<00:00, 2790.67it/s]

    nombre de pos dans le corpus de reference : 10354
    nombre de pos dans le corpus a evaluer : 10354
    l'accuracy est à 100.0%
    la precision pour la classe 'DET' est à 100.0%
    le rappel pour la classe 'DET' est à 100.0%

    real    0m5,899s
    user    0m5,780s
    sys     0m0,733s
    ```
    - module python `timeit` : j'ai utilisé le module tqdm, sinon possibilité de rajouter dans le script :
    ```python
    import timeit
    print(timeit.timeit(stmt='get_conllu("fr")', setup='from __main__ import get_conllu', number=1))
    ```
    ```shell
    (project) laura@laura:~/Documents/TALA540A$ python script/tp1.py 
    phrases conllu: 100%|██████████████████████| 456/456 [00:00<00:00, 43702.65it/s]
    0.27867681899806485
    ```

- matrice de confusion
    - avec pandas
    - avec seaborn pour avoir de jolies couleurs

- comparer
    - différents modèles spacy : on peut choisir le modèle en argument (sm, md, lg, trf)
    - différents corpus UD : français et chinois

### étape 4 : ok
- découpage possible par corpus en fonction du corpus d'où vient chaque phrase
    - corpus fr :
        - Europar
        - annodis
        - emea
        - frwiki
    - corpus zh :
        - n01...
        - w01...
        - n02...
        - n03
        - n04...
        - n05...
        - w02...
        - w03...
        - w04...
        - w05...

- autres petites choses à faire
    - pyJoules : je crois ça marche ?
    ```shell
    phrases spacy: 100%|██████████████████████████| 456/456 [00:08<00:00, 51.46it/s]
    begin timestamp : 1697839169.4288712; tag : get_spacy_retok; duration : 14.85051441192627; package_0 : 89081864.0; dram_0 : 3829275.0; core_0 : 54152877.0; uncore_0 : 785337.0
    ```
    - pylint : critique code pour le rendre lisible
    - mypy : relatif à toutes les annotations de type
    - black : edite code à notre place pour que pylint soit content