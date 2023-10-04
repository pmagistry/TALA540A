### Stanza
* Collection d'outils pour l'analyse linguistique

* Dévelopée en python, propose des modèles neuronaux

* Interface python pour le package java CoreNLP

* première version en 2019, dernière version (1.4) avril 2022

* #### Type de tâches  : 
  * analyse morphosyntaxique, 
  * analyse syntaxique en dépendance, 
  * entités nommées, 
  * segmentation, tokenisation, lemmatisation, 
  * analyse de sentiments

  Avec le package CoreNLP :
  * Parsing en constituant
  * Résolution de coréférence
  

* #### Installation :
pip :
 ```
pip install stanza
```
conda :
```
conda install -c standfordnlp stanza
```
Depuis le dépot git (permet plus de flexibilité et nécéssaire si on veut entraîner des modèles):
```
git clone https://github.come/stanfordnlp/stanza.git
cd stanza
pip install -e
```
* #### Langues traitées :
Modèles pré-entraînés pour 70 langues mais pas tous les modèles pour toutes les langues par exemple l'analyse de sentiment y'a que 3 langues : anglais, chinois, allemand. 
```py
stanza.download("fr")
nlp = stanza.Pipeline("fr", processors = ["tokenize", "pos", "lemma", "ner"])
```


* #### Évaluation :
Évaluations pour toutes les langues et toutes les tâches disponibles sur le site + ils donnent le corpus sur lequel le modèle a été évalué, il s'agit des treebanks d'Universal Dependencies: https://stanfordnlp.github.io/stanza/performance.html
On a aussi les performances sur les versions précédentes pour pouvoir comparer


* #### Utilisation :

```py
import stanza
#stanza.download("fr")#Download French language model

annotate=stanza.Pipeline("fr",processors="tokenize,mwt,pos,lemma,depparse,ner",download_method=None)

sents=annotate("Bienvenue dans le cours de Document Strcturé. Il s'agit d'un cours enseigné par Pierre Magistry.")#À terme, le corpus sera ici

#On itère à travers l'annotation du corpus pour
# noter les informations dans le string output (tableau .tsv)
# et préparer les données pour les arbres de dépendances dans la liste de dictionnaire sentsDependency
output="token\tpos\tfeats\tlemma"
sentsDependency=[]
for sentIndex,sent in enumerate(sents.sentences):
    sentsDependency.append({"heads":{},"id":{}})
    for word in sent.words:
        output+=f"\n{word.text}\t{word.upos}\t{word.feats}\t{word.lemma}"
        try:sentsDependency[sentIndex]["heads"][word.head].append(word)
        except:sentsDependency[sentIndex]["heads"][word.head]=[word]
        sentsDependency[sentIndex]["id"][word.id]=word

outputNER=""
for ent in sents.ents:
    outputNER+=f"\nEntity: {ent.text}\tType: {ent.type}"

print(output)
print(outputNER)
```