# TP1 - eval - Spacy POS tagging

## Étape 1

Récupérer modèle et données.

- [x] Installer Spacy.
- [x] Installer le modèle français.
- [x] Trouver du corpus.
  - Commande :  
    `wget https://github.com/UniversalDependencies/UD_French-Sequoia/raw/master/fr_sequoia-ud-test.conllu`

## Étape 2

Être capable de lire le corpus, charger les Docs Spacy et appliquer un modèle.

- [x] Lire le corpus.
- [x] Charger les Docs Spacy.
- [x] Appliquer un modèle.
- [x] Utiliser typing et dataclasses.

  --> Nayant pas compris les consignes je n'ai pas pu faire le travail demandé.

  Ce que j'ai fais :

  - Nettoyer le corpus téléchargé avec le script `traitement-text.py` puis appliquer un modéle spacy sur le texte.
  - Comparer avec le celui de conllu, script `eval.py`.

    --> Résultats pas du tout concluants.

## Étape 3

Qualifier les résultats.

- [ ] exatitude.
- [ ] vitesse.
- [ ] matrice de confusion.
- [ ] comparer les modéles spacy et les différents corpus.
