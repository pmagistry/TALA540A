#!/usr/bin/env bash

#==============================================================================
# fichier_train -- ./path/to/fichier.conllu : le fichier conllu de train
# fichier_dev -- ./path/to/fichier.conllu : le fichier conllu de dev
# spacy_output -- ./path/to/dossier : le dossier où déposer l'output spacy
# langue -- str : la langue du fichier conllu -- chinese ou french
#==============================================================================


fichier_train=$1 #./corpus/fr_sequoia-ud-train.conllu
fichier_dev=$2 #./corpus/fr_sequoia-ud-dev.conllu
spacy_output=$3 #./script/spacy/
langue=$4 #french

python -m spacy convert $fichier_train $spacy_output -c conllu -l $langue
python -m spacy convert $fichier_dev $spacy_output -c conllu -l $langue