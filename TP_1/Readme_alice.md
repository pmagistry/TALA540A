Lancement du script

Dans le répertoire qui contient les fichiers textes `fr_sequoia-ud-test.conllu` et `corpus_a_tester.txt` ainsi que le fichier `datastruct.py`.

Le fichier `corpus_a_tester.txt` est la version en texte brut du fichier `fr_sequoia-ud-test.conllu`, il a été obtenu avec la manipulation suivante  : 

`cat fr_sequoia-ud-test.conllu | grep "# text" | sed 's/# text = //`

`corpus_a_tester.txt`est notre corpus de test et fr_sequoia-ud-test.conllu` notre corpus de référence.



On segmente le texte de test avec le modèle de Spacy qui étiquète également. On range les formes, lemmes et pos dans un objet Token préparé avec une classe.

On extrait les formes, lemmes et pos du texte sequoia (format connell), avec les regex et on les range dans un objet Token également.

A l'issue de la tokenisation, en faisant un affichage des 15 derniers tuples de forme-pos, on note que la tokénisation avec Spacy n'a pas séparé une ponctuation,un tiret même 2 mots, lorsque Connell a bien tokénisé.

> <u>Spacy :</u>
> 
> [('Indochine', 'PROPN'), ('"', 'PUNCT'), (',', 'PUNCT'), ('Plon', 'PROPN'), (',', 'PUNCT'), ('Paris', 'PROPN'), (',', 'PUNCT'), **('1979.Liens', 'NUM')**, (**'internes-', 'NOUN'**), ('Colloque', 'PROPN'), ('sur', 'ADP'), ('les', 'DET'), **('fraudesQuatrième',** 'ADJ'), ('République', 'PROPN'), ('.', 'PUNCT')]
> 
> <u>Connell  :</u>
> [(',', 'PUNCT'), ('Paris', 'PROPN'), (',', 'PUNCT'), **('1979', 'NUM'), ('.', 'PUNCT')**, ('Liens', 'NOUN'), **('internes', 'ADJ'), ('-', 'PUNCT'),** ('Colloque', 'NOUN'), ('sur', 'ADP'), ('les', 'DET'), **('fraudes', 'NOUN'), ('Quatrième', 'ADJ')**, ('République', 'NOUN'), ('.', 'PUNCT')]

De fait, on obtient des tailles respectives de **9 525 tokens **pour la liste de tuple Spacy et **10 354 tokens **pour Connell.

Il y a un décalage lorque l'on itère sur les tuples, comment faire une comparaison sur les pos des mêmes tokens dans ce cas? on fait un test sur chaque token pour voir si il s'agit bien du même token dans les 2 listes mais on perd

Le résultat est très mauvais, il faut revoir la segmentation et ajouter des règles pour améliorer. 
