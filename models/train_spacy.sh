#!/usr/bin/env bash

# toutes les commandes pour entrainer le modèle spacy depuis le dossier TALA540A :
# 		$ ./models/train_spacy.sh

# pour la partie config
# python -m spacy init fill-config ./models/spacy/base_config_acc.cfg ./models/spacy/config_acc.cfg

# transformer les corpus si ce n'est pas déjà fait
python -m spacy convert ./corpus/lzh_kyoto-ud-train.conllu ./corpus/spacy_corpus/ -c conllu -l chinese -n 10
python -m spacy convert ./corpus/lzh_kyoto-ud-dev.conllu ./corpus/spacy_corpus/ -c conllu -l chinese -n 10

# lancer l'entrainement
python -m spacy train ./models/spacy/config_acc.cfg --output ./models/spacy/monmodel/ --paths.train ./corpus/spacy_corpus/lzh_kyoto-ud-train.spacy --paths.dev ./corpus/spacy_corpus/lzh_kyoto-ud-dev.spacy