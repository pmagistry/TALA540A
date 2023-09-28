# first project

## groupe
- Alice Wallard
- Laura Darenne
- Li Kedi
- Liza Fretel

Tous les outils ont été développé particulièrement pour le chinois mais certains ont des modèles anglais. Nous avons testé les modèles chinois

## n-ltp = outils open-source présent sur git-hub

### urls
- https://aclanthology.org/2021.emnlp-demo.6/
- https://github.com/HIT-SCIR/ltp/blob/main/python/interface/README.md

### téléchargement
```
# installer les dépendances pytorch et transformers
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple torch transformers

# installer ltp
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ltp ltp-core ltp-extension
```
### d’où vient cet outils
- présent sur github (issues...)
- open-source
- article acl pour présenter le projet
- créé par deux étudiants chinois pour faire les choses suivantes :
	- chinese word segmentation, 
	- part-of-speech tagging, 
	- named entity recognition
	- syntactic parsing (dependency parsing)
	- semantic dependency parsing
	- semantic role labeling

### quel type de sorti il propose
```
# cws : segmentation de mots
# pos : partie du discours 
# ner : annotation d'entité nommée 
# srl : annotation de rôle sémantique
# dep : analyse de syntaxe de dépendance
# sdp : arbre d'analyse de dépendance sémantique
# sdpg : graphique d'analyse de dépendance sémantique
```

### comment ça marche
```
import torch
from ltp import LTP

# telecharge par defaut le modèle depuis huggingface
# charge par default le petit modèle
# sinon ltp = LTP("/path/to/your/model")
ltp = LTP("LTP/small")  

# si gpu.............
if torch.cuda.is_available():
    # ltp.cuda()
    ltp.to("cuda")

output = ltp.pipeline(["他叫汤姆去拿外衣。"], tasks=["cws", "pos", "ner", "srl", "dep", "sdp", "sdpg"])
print(output.cws) # avec indices ou version dict : print(output[0]) / print(output['cws'])
print(output.pos)
print(output.ner)
print(output.srl)
print(output.dep)
print(output.sdp)
print(output.sdpg)
```
```
[['他', '叫', '汤姆', '去', '拿', '外衣', '。']]
[['r', 'v', 'nh', 'v', 'v', 'n', 'wp']]
[[('Nh', '汤姆')]]
[[{'predicate': '叫', 'arguments': [('A0', '他'), ('A1', '汤姆'), ('A2', '去拿外衣')]}, {'predicate': '拿', 'arguments': [('A0', '汤姆'), ('A1', '外衣')]}]]
[{'head': [2, 0, 2, 5, 2, 5, 2], 'label': ['SBV', 'HED', 'DBL', 'ADV', 'VOB', 'VOB', 'WP']}]
[{'head': [2, 0, 2, 2, 4, 5, 2], 'label': ['AGT', 'Root', 'DATV', 'eSUCC', 'eSUCC', 'PAT', 'mPUNC']}]
[[(1, 2, 'AGT'), (2, 0, 'Root'), (3, 2, 'DATV'), (3, 4, 'AGT'), (3, 5, 'AGT'), (4, 2, 'eSUCC'), (5, 2, 'eSUCC'), (5, 4, 'eSUCC'), (6, 5, 'PAT'), (7, 2, 'mPUNC')]]
```
- possible d'utiliser l'indentation ou `output.qqchose`
- certains résultats sont en liste, liste de tuples ou dictionnaires
- resultat brut quand on fait `print(output)`
```
LTPOutput(
	cws=[['他', '叫', '汤姆', '去', '拿', '外衣', '。']], 
	pos=[['r', 'v', 'nh', 'v', 'v', 'n', 'wp']], 
	ner=[[('Nh', '汤姆')]], 
	srl=[[{'predicate': '叫', 'arguments': [('A0', '他'), ('A1', '汤姆'), ('A2', '去拿外衣')]}, {'predicate': '拿', 'arguments': [('A0', '汤姆'), ('A1', '外衣')]}]], 
	dep=[{'head': [2, 0, 2, 5, 2, 5, 2], 'label': ['SBV', 'HED', 'DBL', 'ADV', 'VOB', 'VOB', 'WP']}], 
	sdp=[{'head': [2, 0, 2, 2, 4, 5, 2], 'label': ['AGT', 'Root', 'DATV', 'eSUCC', 'eSUCC', 'PAT', 'mPUNC']}], 
	sdpg=[[(1, 2, 'AGT'), (2, 0, 'Root'), (3, 2, 'DATV'), (3, 4, 'AGT'), (3, 5, 'AGT'), (4, 2, 'eSUCC'), (5, 2, 'eSUCC'), (5, 4, 'eSUCC'), (6, 5, 'PAT'), (7, 2, 'mPUNC')]]
	)
```

```
# une version avec la segmentation des mots, la reconnaissance de parties du discours et d'entités nommées relativement + rapide, mais une précision est légèrement inférieure
# algorithme perceptron qui ne fait pas plus que cws, pos, net
ltp = LTP("LTP/legacy")

cws, pos, ner = ltp.pipeline(["他叫汤姆去拿外衣。"], tasks=["cws", "pos", "ner"]).to_tuple()
print(cws, pos, ner)
```
```
[['他', '叫', '汤姆', '去', '拿', '外衣', '。']] [['r', 'v', 'nh', 'v', 'v', 'n', 'wp']] [[('Nh', '汤姆')]]
```
- resultat brut quand on fait :
```
print(ltp.pipeline(["他叫汤姆去拿外衣。"], tasks=["cws", "pos", "ner"]).to_tuple())
```
```
(
	[['他', '叫', '汤姆', '去', '拿', '外衣', '。']], 
	[['r', 'v', 'nh', 'v', 'v', 'n', 'wp']], 
	[[('Nh', '汤姆')]]
)
```

## deep-nlp

## url
- https://github.com/rockingdingo/deepnlp

## téléchargement
- pour télécharger le module : `pip install deepnlp`
- pour télécharger les modèles directement sur le script python
```
import deepnlp
# Download all the modules
deepnlp.download()

# Download specific module
deepnlp.download('segment')
deepnlp.download('pos')
deepnlp.download('ner')
deepnlp.download('parse')

# Download module and domain-specific model
deepnlp.download(module = 'pos', name = 'en')
deepnlp.download(module = 'ner', name = 'zh_entertainment')
```

### d’où vient cet outils
- présent sur git
- pas d'informations sur son developpeur

### quel type de sorti il propose
- Word Segmentation/Tokenization
- Part-of-speech (POS)
- Named-entity-recognition(NER)
- Dependency Parsing (Parse)
- textsum: automatic summarization Seq2Seq-Attention models
- textrank: extract the most important sentences
- textcnn: document classification
- Web API: Free Tensorflow empowered web API
- Planed: Automatic Summarization

### si on arrive à faire marcher, comment ça marche
- cet outils ne marche pas sur nos machines
- `deepnlp` n'est plus mis à jour depuis 6 ans (dernier commit en janvier 2018) et dernière issue fermée par le dev en 2018
- le module est encore téléchargeable mais il ne marche pas à cause du module `crfpp` :
	- issue ouverte depuis 2 ans sur le git de deepnlp : "No module named 'CRFPP'"
	- le module `crfpy` installable via pip n'est plus  telechargeable, le dossier git dont il est issu n'est plus disponible
  - le module `crf++` contenant lui aussi `crfpp` n'est plus mise à jour depuis 2013
  - le module `crfpp` qui est téléchargeable en clonant le dossier git `deepnlp` n'est plus installable, il se télécharge d'une manière que python ne prend plus en charge (`python setup.py install`)

- pour la segmentation :
  ```
from deepnlp import segmenter

tokenizer = segmenter.load_model(name = 'zh_entertainment')
text = "我刚刚在浙江卫视看了电视剧老九门，觉得陈伟霆很帅"
segList = tokenizer.seg(text)
text_seg = " ".join(segList)

#Results
# 我 刚刚 在 浙江卫视 看 了 电视剧 老九门 ， 觉得 陈伟霆 很 帅
  ```
- pour les entités nommées :
```
import deepnlp
deepnlp.download('ner')  # download the NER pretrained models from github if installed from pip

from deepnlp import ner_tagger

# Example: Entertainment Model
tagger = ner_tagger.load_model(name = 'zh_entertainment')   # Base LSTM Based Model
#Load Entertainment Dict
tagger.load_dict("zh_entertainment")
text = "你 最近 在 看 胡歌 演的 猎场 吗 ?"
words = text.split(" ")
tagset_entertainment = ['actor', 'role_name', 'teleplay', 'teleplay_tag']
tagging = tagger.predict(words, tagset = tagset_entertainment)
for (w,t) in tagging:
    pair = w + "/" + t
    print (pair)

#Result
#你/nt
#最近/nt
#在/nt
#看/nt
#胡歌/actor
#演的/nt
#猎场/teleplay
#吗/nt
#?/nt
```
...

## DDParser

### url
- [https://github.com/baidu/DDParser](https://github.com/baidu/DDParser)
- [https://pypi.org/project/ddparser/](https://pypi.org/project/ddparser/)

## téléchargement
- installer ddparser : `pip install ddparser`
- installer paddlepaddle avec ou sans cuda : 
	- `nvcc --version` + https://www.paddlepaddle.org.cn/
	- `pip install paddlepaddle==2.4.2
- installer LAC : `pip install lac`

### d’où vient cet outils
- Développé par l'entreprise Baidu
- Disponible sur Github
- open-source
- Les données utilisées par l'outil pour entraîner son modèle est Baidu Chinese Treebank 1.0. Il est composé d'un million de phrases mais l'outil en a utilisé 530k. Ce sont des données issues du web, écrites comme orales, des news, des forums etc.

### quel type de sorti il propose (quel type d’informations)
DDParser est utilisé pour faire de l'analyse syntaxique.
Il intègre un outil de tokenisation et de POS tagging, qui sont les étapes précédentes et nécessaires à l'analyse syntaxique.
#### Compatibilité CoNLL-X
La sortie est compatible avec le format CoNLL:
```
ID      FROM   LEMMA CPOSTAG POSTAG  FEATS   HEAD    DEPREL   PROB   PDEPREL
1       百度    百度    -       -       -       2       SBV     1.0     -
2       是      是      -       -       -       0       HED     1.0     -
3       一家    一家    -       -       -       5       ATT     1.0     -
4       高科技  高科技  -       -       -       5       ATT     1.0     -
5       公司    公司    -       -       -       2       VOB     1.0     -
```

#### Format de sortie

En sortie de la fonction parse ou parse_seg, on obtient une liste dont chaque élément est une phrase.
Dans cette liste, un dictionnaire avec 3 clés:
- 'word', avec pour valeur la liste des tokens.
- 'head', avec pour valeur une liste: pour chaque token, quelle est l'indice de la tête de la relation dans l'arbre syntaxique. 0 pour la racine.
- 'deprel', avec pour valeur une liste: pour chaque token, quelle est l'étiquête de la relation avec sa tête.
Exemple:
```
[{'word': ['百度', '是', '一家', '高科技', '公司'], 'head': [2, 0, 5, 5, 2], 'deprel': ['SBV', 'HED', 'ATT', 'ATT', 'VOB']}, {'word': ['他', '送', '了', '一本', '书'], 'head': [2, 0, 2, 5, 2], 'deprel': ['SBV', 'HED', 'MT', 'ATT', 'VOB']}]
```

### si on arrive à faire marcher, comment ça marche
- nous avons rencontré plusieurs problèmes :
	- avec paddle 2.5.1 :
		- `libssl.so.1.1: cannot open shared object file: No such file or directory`
			- solution :
			- `wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb`
			- `sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb`
		- `AttributeError: module 'paddle.fluid.dygraph' has no attribute 'Layer'` 
			- impossible de trouver de solution
			- dans les issues sur le github, beaucoup de personnes ont des problèmes avec la classe `fluid`
	- avec paddle 2.4.2 :
		- marche à peu près mais des problèmes (Warnings) au niveau du téléchargement des modules car le python sur lequel ont travaille est trop haut

- sinon, marche comme cela :
```
from ddparser import DDParser
ddp = DDParser() # ajouter l'argument use_cuda=True pour utiliser un GPU.
		 # ajouter l'argument buckets=True pour accélérer le traîtement d'un grand nombre de données de taille inégale.
#### Une seule phrase
ddp.parse("百度是一家高科技公司")
#### Plusieurs phrases
ddp.parse(["百度是一家高科技公司", "他送了一本书"])
#### On peut aussi avoir des phrases pré-tokenisées (par un autre outil par exemple)
ddp.parse_seg([['百度', '是', '一家', '高科技', '公司'], ['他', '送', '了', '一本', '书']])

```
