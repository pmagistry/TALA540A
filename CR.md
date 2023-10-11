# CR du TP1 - Amaury GAU

## Première étape 

Cette première partie de script s'est basée tout d'abord sur des datastructures de classes : 
- Corpus(text : str, sents : List[Sent]) 
- Sent(text : str, tokens : List[Token])
    dep : str
- Token(id : int, text : str, lemma : str, pos : str, head : int, misc : str)

Pour les tokens, j'ai préféré garder une grande partie des informations présentes dans le conll, notamment la gestion du misc, qui permet, si bien annoté, de connaôtre la présence d'espaces ou non après le token annoté. Cette information est notamment utile pour la classe Doc de Spacy. 

## Deuxième étape 

Extraire les informations du fichier .conll et les intégrer et créer ma classe corpus. 
Je pense que cette étape n'a pas été si difficile, sauf pour la classe misc, qui a été un challenge au début. En effet, je n'avais pas fait attention que selon l'information entrée à l'intérieur, j'avais soit une donnée de type \<dict> soit de type \<NoneType>. Il a donc fallu que j'ajoute une troisième fonction pour traiter et construire mes tokens. 

Cela a d'ailleurs été l'occasion de choisir quelle était l'information à garder dans cette classe. J'ai choisi de m'aligner sur la variable _spaces_ de la classe Doc de Spacy. Mes token["misc"] sont donc des booléens correspondant à ce qu'attend spacy. 

## Troisième étape 

Il faut maintenant aligner les données pour les comparer. 
Je me suis d'abord mépris en pensant qu'il fallait recréer une classe Doc à partir de 0 à partir des données extraites du conll. Mais beaucoup d'erreurs sont apparues. Notamment, le fait que les données n'étaient pas alignées. En effet, bien que les nombres de tokens et de pos soit bien égaux dans l'annotation conll, les prépositions amalgamées avec le déterminant (ex : du = de + le) était annotées par "_" en tant que POS, et ensuite détaillées par la suite avec les bon POS, respectivement ADP et DET. 

Malheureusement, pour la classe Doc de Spacy, il est impossible d'avoir des POS différents que ceux du conll, et "_" n'est pas reconnu comme un POS. L'alignement via la classe Doc ne pouvant pas avoir lieu, j'ai abandonné d'utiliser cette classe Spacy. 

## Quatrième étape 

J'ai donc décidé d'aligner les annotations créées par la prédiction de spacy, avec les annotations extraites de notre corpus conll. 
La méthode algorithmique n'est pas très belle, mais fonctionne. 
J'ai aussi découvert, à mon grand regret, qu'il était impossible d'incrémenter des tuples... Ce qui m'a rajouté pas mal de lignes de code. Une fonctione d'incrémentation de compteurs reste en commentaire de mon code comme preuve de son passage. 

## Calcul de l'exactitude 

J'ai aligné les pos de conll avec les prédictions de spacy. Si la longueur des listes est égale, alors on compare pos à pos. 
- correct += 1 si les pos sont égaux ; error +1 si les pos ne coïncident pas   

Si les listes ne sont pas de même longueur (par exemple pour le cas de nos fameuses prépositions amalgamées) : 

- error += la différence de longueur entre les deux listes. 
- On compare les pos jusqu'à la fin de la liste la plus courte 
- correct += 1 si les pos sont égaux ; error +1 si les pos ne coïncident pas   

#### Résultat 
La formule utilisée est celle de l'exactitude, et reportée sur nos variables, et la suivante : 

$$
Exactitude=\frac{\text{nombre de pos corrects}}{\text{corrects + errors}} = \frac{6289}{6289+3904}=0.617
$$.

Suivant ce test, on peut dire que l'exactitude du modèle est bien plus basse que l'évaluation de spacy elle-même. 
Toutefois, l'écart est tellement grand, que j'ai probablement commis une erreur quelque part. 
Je revérifierai mes algorithmes ultérieurement
