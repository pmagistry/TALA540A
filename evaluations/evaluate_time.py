#!/usr/bin/env python
# coding: utf-8

"""
    Ce que l'on peut ecrire sur le terminal depuis le dossier TALA540A :
    $ python evaluations/evaluate_time.py
    
    Ce fichier permet de mesurer le temps de chargement et d'analyse des modèles (avec time)
    et leur empreinte énergétique
"""

from pyJoules.energy_meter import measure_energy

@measure_energy
def main():
    
    # les modèles
    # (corpus_r, "corpus_lg", "zh_core_web_lg", "GREEN")
    # (corpus_r, "corpus_md", "zh_core_web_md", "CYAN")
    # (corpus_r, "corpus_sm", "zh_core_web_sm", "MAGENTA")
    # (corpus_r, "corpus_trf", "zh_core_web_trf", "RED")
    # (corpus_r, "corpus_jiayan", "./models/jiayan/modele_jiayan", "BLUE")
    # (corpus_r, "corpus_sentence", "./models/jiayan/modele_sentence", "YELLOW")
    # (corpus_r, "corpus_table", "./models/jiayan/modele_table", "GREEN")
    # (corpus_r, "corpus_word", "./models/jiayan/modele_word", "RED")
    # (corpus_r, "corpus_modele1", "./models/spacy/modele1/model-best", "RED")
    # (corpus_r, "corpus_modele2", "./models/spacy/modele2/model-best", "RED")
    # (corpus_r, "corpus_modele3", "./models/spacy/modele3/model-best", "RED")
    # (corpus_r, "corpus_modele4", "./models/spacy/modele4/model-best", "RED")
    # (corpus_r, "corpus_modele5", "./models/spacy/modele5/model-best", "RED")
    # (corpus_r, "corpus_modele6", "./models/spacy/modele6/model-best", "RED")
    # (corpus_r, "corpus_modele7", "./models/spacy/modele7/model-best", "RED")
    # (corpus_r, "corpus_modele8", "./models/spacy/modele8/model-best", "RED")
    # (corpus_r, "corpus_modele9", "./models/spacy/modele9/model-best", "RED")
    # (corpus_r, "corpus_modele10", "./models/spacy/modele10/model-best", "RED")

    corpus_train = get_conllu("train")
    vocabulaire = {token.form for sentence in corpus_train.sentences for token in sentence.tokens}
    corpus_r = get_conllu("test", vocabulaire)
    get_jiayan(corpus_r, "corpus_jiayan", "./models/jiayan/modele_table", "BLUE")

if __name__ == "__main__":
    main()