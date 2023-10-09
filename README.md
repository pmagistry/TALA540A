# TALA540A

## TP1 de Laura Darenne

### liste des fichiers
- README.md : explications du tp
- TP_eval.md : étapes du tp à faire

#### python
- tp1.py : fichier python principal du projet
- get_function.py : fichier python avec toutes les fonctions appelées par tp1.py
- datastructures.py : fichier python contenant les dataclasses appelées par get_function.py

#### corpus
- fr_sequoia-ud-test.conllu  
- textebrut.txt  

---

### étape 1
- texte téléchagé
- texte brut de fr_sequoia-ud-test.conllu copié dans le fichier textebrut.txt

---

### étape 2
- tokenisation et analyse du texte avec spacy :
- recuperation des données du fichier conllu

- tokenization avec le fichier conllu tout en utilisant spacy :
    - forcement, c'est plus rapide car on va juste chercher des informations dans une variable contenant le texte du fichier conllu

---

### étape 3

- exactitude :
    - accuracy ; precision et rappel pour le pos 'DET'
    - **idem en distanguant les OOV : à faire mais peut-être pas le temps**

- vitesse
    - bash `time` : n'a pas marché correctement
    ``` Shell
        (project) laura@laura:~/Documents/TALA540A$ time script/tp1.py
            bash: script/tp1.py: Permission denied

            real    0m0,002s
            user    0m0,001s
            sys 0m0,000s

    ```
    - module python `timeit` : j'ai utilisé le module tqdm, sinon :
    ```python
    import timeit
    print(timeit.timeit(stmt="get_spacy()", setup="from __main__ import get_spacy", number=1))
    ```

