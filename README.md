# POS_Tagging_Bengali
### Document structuré

Comparaison des outils pour le POS tagging de bengali 

Nécessite: 
1. sudo chmod -R a+r /sys/class/powercap/intel-rapl 
2. python3 bn_eval_basique.py 
	- Essai adaptation Spacy , mais avec modèle entraîné par hindi
3. python3 pos_tagging_with_banglanltk.py
	- extraction des pos, avec les bibliothèques **bnlp** et **banglanltk** en format Corpus du module bn_eval_basique
	- calcul et affichage de l'accuracy 
4. creation des fichiers bn_train_corpus.conllu et bn_dev_corpus.conllu 
	- conversion spacy échoué

	
	

