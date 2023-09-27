# Fiches de synthèse - Outils TAL


**Nom de l'outil** : KoNLPy
**Version** : 0.6.0
**Créé le** : 26 août 2014
**Dernière mise à jour le** : 2 janvier 2022
**Accessibilité** : Open Source (under GPL licence)
**Auteurs** : Park Eunjeong L. and Cho Sungzoon
**Outil associé aux institutions** : 
**Lien du site internet** : https://konlpy.org/en/latest/ 
**Références** :
- Eunjeong L. Park, Sungzoon Cho. “KoNLPy: Korean natural language processing in Python”, Proceedings of the 26th Annual Conference on Human & Cognitive Language Technology, Chuncheon, Korea, Oct 2014 - (plus trouvable sur internet)
- https://buildmedia.readthedocs.org/media/pdf/konlpy/stable/konlpy.pdf
- Kim, Hung-gyu, et al. “21st Century Sejong Corpora (to Be) Completed.” The Korean Language in America, vol. 12, 2007, pp. 31–42. JSTOR, http://www.jstor.org/stable/42922169. Accessed 27 Sept. 2023.
- http://semanticweb.kaist.ac.kr/home/index.php/Corpus1


**Utilisation de différents modules** : 
- KKMA (utilisation d’un dictionnaire créé à partir du corpus Sejong) : analyseur morpho-syntaxique développé en Java par Intelligent Data Systems (IDS) à l’Université Nationale de Séoul (SNU).
	- Corpus Sejong (1997-2007) : Se veut devenir le corpus national coréen (au même niveau que le British National Corpus. Composé de textes bruts et annotés provenant de différents domaines : coréen moderne (écrit et transcription orale), nord-coréen, coréen utilisé à l’étranger, vieux coréen, corpus parallèles (alignés par phrase) coréen-japonais et coréen-anglais, coréen spécialisé. ~ 89 millions de mots bruts. Créé par l’Institut National de la Langue Coréenne
- Hannamun (utilisation d’un dictionnaire créé à partir du corpus KAIST) : analyseur morpho-syntaxique et POS-Tagger développé en Java par le SWRC (Semantic Web Research Center)  à l’Institut supérieur coréen des sciences et technologies (KAIST)(1999-2014)
	- Corpus KAIST (1994-1997) : corpus composé de textes bruts tirés de romans, d’articles de presse, etc. ~ 70 millions de mots
	- Options
		- .analyze(phrase) : recherche dictionnaire et segmentation des termes non reconnus
		- .morphs(phrase) : créer une liste des morphèmes présents dans la phrase
		- .nouns(phrase) : extraction des noms
		- .pos(phrase) : associe une étiquette à chaque morphème (de manière probabiliste).
- Mecab(utilisation d’un dictionnaire créé à partir du corpus Sejong) : analyseur morphologique et POS-tagger développé à l’origine pour le japonais par la Graduate School of Informatics de l’université de Kyoto puis modifié par le projet Eunjeon pour l’adapter au coréen
	- Options : 
		- .morphs(phrase) : créer une liste des morphèmes présents dans la phrase
		- .nouns(phrase) : retourne une liste des noms présents dans la phrase
		- .pos(phrase) : retourne une liste de tuples où chaque tuple est composé du token et de son étiquette de partie du discours. 
- Komoran (possibilité d’utiliser un dictionnaire utilisateur) : 
- Okt (Open Korean Text) : tokenizer open source du coréen, écrit en Scala et développé par Will Hohyon Ryu.
	- Options
		- .morphs(phrase) : créer une liste des morphèmes présents dans la phrase
		- .nouns(phrase) : retourne une liste des noms présents dans la phrase
		- .phrases(phrase) : retourne une liste contenant plusieurs découpages possibles de la phrase, ajoutant les syntagmes au fur et à mesure + les noms à la fin de la liste
		- .pos(phrase) : retourne une liste de tuples où chaque tuple est composé du token et de son étiquette de partie du discours. 
			- norm=True : normalise les tokens
			- stem=True : stemmatisation des tokens
			- join=True : retourne des ensembles joints de morphèmes et d’étiquettes (?)

**Tâches propres à KoNLPy** : 
- konlpy.corpus → contient des corpus coréen
- konlpy.utils : 
	- .char2hex(c) →Conversion en code hexadécimal
	- .hex2char(hex) →inverse
	- .concordance(chaîne de caractères, document, show=True) : affiche les occurrences d’une chaîne de caractère dans le document et son contexte
	- .delete_links(text) → suppression des liens
	- …


---

**Nom de l’outil** : Mecab python (Origine : Mecab)
**Version** : 1.08 (0.96)
**Sortie initiale** : 2014-09-11 (2006-03-26)
**Dernière MàJ** : 2023-09-22 (2013-02-18)
**Accessibilité** : Logiciel libre (Licences GPL, LGPL, BSD) 
**Auteur** : Kudo Taku 
**Outil associé aux institutions** : NTT Corporation
**Lien du site internet** : https://pypi.org/project/mecab-python3/#description 
**Références** : 
- Kudo, Taku, Jun Suzuki, et Hideki Isozaki. 2005. « Boosting-based Parse Reranking with Subtree Features ». In Proceedings of the 43rd Annual Meeting of the Association for Computational Linguistics (ACL’05), 189‑96. Ann Arbor, Michigan: Association for Computational Linguistics. https://doi.org/10.3115/1219840.1219864.
- Taku Kudo. 2006. Mecab: Yet another part-of-speech and morphological analyzer. http://taku910.github.io/mecab/.

**Dictionnaires utilisés** : 
- Juman (plus maintenu depuis 2014) 
- IPADic (plus maintenu depuis 2007) 
- Unidic (2007 -) 

**Description** : librairie python permettant d’utiliser l’analyseur morphologique pour le japonais MeCab


---

Bengali 

Outil : bnlp 
github : https://github.com/sagorbrur/bnlp

Bibliothèque assez complet

Corpus :
https://wortschatz.uni-leipzig.de/en/download/Bengali

