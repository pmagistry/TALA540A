#!/usr/bin/env bash

#==============================================================================
# fichier_train -- ./path/to/fichier.conllu : le fichier conllu de train
# fichier_dev -- ./path/to/fichier.conllu : le fichier conllu de dev
# spacy_output -- ./path/to/dossier : le dossier où déposer l'output de spacy
# langue -- str : la langue du fichier conllu -- chinese ou french
#==============================================================================

# ./script/corpus_and_train.sh ./corpus/fr_sequoia-ud-train.conllu ./corpus/fr_sequoia-ud-dev.conllu ./script/model_spacy/corpus/ french
# ./script/corpus_and_train.sh ./corpus/zh_gsdsimp-ud-train.conllu ./corpus/zh_gsdsimp-ud-dev.conllu ./script/model_spacy/corpus/ chinese


fichier_train=$1 #./corpus/fr_sequoia-ud-train.conllu
fichier_dev=$2 #./corpus/fr_sequoia-ud-dev.conllu
spacy_output=$3 #./script/model_spacy/corpus/
langue=$4 #french

python -m spacy convert $fichier_train $spacy_output -c conllu -l $langue
python -m spacy convert $fichier_dev $spacy_output -c conllu -l $langue

if [[ $langue == "chinese" ]]
then
	python -m spacy train ./script/model_spacy/config_zh.cfg --output ./script/model_spacy/model_zh/ --paths.train ./script/model_spacy/corpus/zh_gsdsimp-ud-train.spacy --paths.dev ./script/model_spacy/corpus/zh_gsdsimp-ud-dev.spacy
else
	python -m spacy train ./script/model_spacy/config_fr.cfg --output ./script/model_spacy/model_fr/ --paths.train ./script/model_spacy/corpus/fr_sequoia-ud-train.spacy --paths.dev ./script/model_spacy/corpus/fr_sequoia-ud-dev.spacy
fi
