#!/usr/bin/env bash

#### toutes les commandes pour entrainer le modèle spacy

# transformer les corpus si ce n'est pas déjà fait
python -m spacy convert ./corpus/lzh_kyoto-ud-train.conllu ./script/model_spacy/corpus/ -c conllu -l chinese -n 10
python -m spacy convert ./corpus/lzh_kyoto-ud-dev.conllu ./script/model_spacy/corpus/ -c conllu -l chinese -n 10

# lancer l'entrainement
python -m spacy train ./script/model_spacy/config.cfg --output ./script/model_spacy/monmodel/ --paths.train ./script/model_spacy/corpus/lzh_kyoto-ud-train.spacy --paths.dev ./script/model_spacy/corpus/lzh_kyoto-ud-dev.spacy