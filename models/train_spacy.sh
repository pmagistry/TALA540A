#!/usr/bin/env bash

# toutes les commandes pour entrainer le modèle spacy depuis le dossier TALA540A :
# 		$ ./models/train_spacy.sh

# pour la partie config
# python -m spacy init fill-config ./models/spacy/base_config_acc.cfg ./models/spacy/config_acc.cfg

# initialisation des corpus au format spacy
# python -m spacy convert ./corpus/lzh_kyoto-ud-train.conllu ./corpus/spacy_corpus/ -c conllu -l chinese -n 5
# python -m spacy convert ./corpus/lzh_kyoto-ud-dev.conllu ./corpus/spacy_corpus/ -c conllu -l chinese -n 5

for num in {6..10}
do
	echo "entrainement modèle $num"

	# initialisation des vecteurs au format spacy
	python -m spacy init vectors zh ./corpus/vectors/word2vec$num.vec ./corpus/spacy_corpus/vectors/

	# lancer l'entrainement
	python -m spacy train ./models/spacy/config_acc.cfg --output ./models/spacy/modele$num/ --paths.train ./corpus/spacy_corpus/lzh_kyoto-ud-train.spacy --paths.dev ./corpus/spacy_corpus/lzh_kyoto-ud-dev.spacy --paths.vectors ./corpus/spacy_corpus/vectors/
done