import spacy
import csv
import pandas as pd

"""avant de lancer une script nous avons besoin de corpus textuel, si vous avez un fichier conllu 
vous pouvez lancer un code cat fichier.conllu | grep "# text" | sed 's/# text = //' > fichier.txt"""

# def annotation_text_spacy_toCSV(fichier_txt) :
# 	"""Cette fonction prend en entrée un fichier txt et retourne un fichier csv avec deux colonnes token et pos"""
# 
# 	with open(fichier_txt, "r") as f_input, open('output_spacy.tsv', 'w', newline='') as f_output:
# 		csv_output = csv.writer(f_output, delimiter='\t')
# 		csv_output.writerow(['token', 'pos'])
#     	
# 		text = f_input.read().splitlines()
# 		nlp = spacy.load("fr_core_news_sm")
# 		for line in text : 
# 			doc = nlp(line)
# 			for token in doc :
# 				tok, pos = token.text, token.pos_
# 				csv_output.writerow([tok,pos])
# 		return f_output.name


def annotation_text_spacy_to_tuples(fichier_txt) :
	"""Cette fonction prend en entrée un fichier txt et retourne une liste de tuples contenant tok et pos"""
	tokpos_list = []
	with open(fichier_txt, "r") as f_input:
		text = f_input.read().splitlines()
		nlp = spacy.load("fr_core_news_sm")
		for line in text : 
			doc = nlp(line)
			for token in doc :
				tok, pos = token.text, token.pos_
				tokpos_list.append((tok,pos))
		return tokpos_list 



# def annotation_conllu_toCSV(fichier_conllu): 
# 	"""Cette fonction prend en entrée un fichier conllu et retourne un fichier csv avec deux colonnes token et pos"""
# 	with open(fichier_conllu, "r") as f_input, open('output_gold.tsv', 'w', newline='') as f_output:
# 		csv_output = csv.writer(f_output, delimiter='\t')
# 		csv_output.writerow(['token', 'pos'])
# 		
# 		text = f_input.read().splitlines()
# 		for line in text :
# 			if not line.startswith("#") and line!="":
# 				token, pos = line.split()[1], line.split()[3]
# 				csv_output.writerow([token,pos])
# 	return f_output.name

def annotation_conllu_to_tuples(fichier_conllu): 
	"""Cette fonction prend en entrée un fichier conllu et retourne une liste de tuples avec token et pos"""
	tokpos_lst = []
	with open(fichier_conllu, "r") as f_input:
		text = f_input.read().splitlines()
		for line in text :
			#condition pour ne pas repérer les formes contractès, car en conllu ils sont divisés p.ex du => de + le.
			if line!="" and not line.startswith("#") and line.split()[3]!="_" :
				token, pos = line.split()[1], line.split()[3]
				tokpos_lst.append((token,pos))
	return tokpos_lst

def comparaison(lst_gold, lst_comp): 
	"""cette fonction prend deux listes de tuples et les comapre en ajoutant tuples null quand besoin"""
	max = len(lst_gold)
	if len(lst_comp) > max :
		max = len(lst_comp)
	tuple = ("null", "null")
	for i in range(len(lst_gold)):
		(tok_gold, pos_gold) = lst_gold[i]
		(tok, pos) = lst_comp[i]
		print(lst_comp[i], lst_gold[i])
		if tok != tok_gold : 
			(tok_gold_next, pos_gold_next) = lst_gold[i+1]
			(tok_next, pos_next) = lst_comp[i+1]
			(tok_gold_next2, pos_gold_next2) = lst_gold[i+2]
			(tok_next2, pos_next2) = lst_comp[i+2]
			if tok_gold_next == tok:
				lst_comp.insert(i,tuple)
			elif tok_gold_next2 == tok:
				lst_comp.insert(i,tuple)
				lst_comp.insert(i,tuple)
			elif tok in tok_gold: 
				lst_gold.insert(i+1,tuple)
			elif tok_gold == "null":
				if tok_gold_next != tok_next:
					lst_gold.insert(i+1,tuple)
			elif tok_gold in tok:
				lst_comp.insert(i+1,tuple)
			elif tok == "null":
				if tok_gold_next != tok_next:
					lst_comp.insert(i+1,tuple)
		#print(lst_gold[i], "///", lst_comp[i])

## dans la fonction il faut plutot faire boucle while qui va tourner jusqua la fin de liste, car en ajoutant des nulls on sort pas de for. alor i est une valeur fixe mais liste est mutable et son longeur ralange dans la boucle.
## ajouter evaluation
	
				
		
#jusqua vitesse

comp_lst = annotation_text_spacy_to_tuples("fr_sequoia-ud-test.txt")
gold_lst = annotation_conllu_to_tuples("fr_sequoia-ud-test.conllu")
print(comparaison(gold_lst,comp_lst))
