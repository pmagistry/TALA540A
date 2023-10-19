#!/bin/python3
# -*- coding: utf-8 -*-

import corpus, conll
import argparse
import sys
import re

from sklearn.metrics import confusion_matrix


def import_spacy(model):
	# Spacy imports
	import spacy
	#from spacy.tokenizer import Tokenizer

	module = __import__(model, fromlist=[model])
	nlp = spacy.load(model)
	return nlp

def evaluate(corpus, model):
	from spacy.tokens import Doc
	nlp = import_spacy(model)
	vocab = set(nlp.vocab.strings)
	total_ok_corpus = 0
	total_wrong_corpus = 0
	# oov
	total_oov_ok_corpus = 0
	total_oov_wrong_corpus = 0

	# for confusion matrux
	y_true = []
	y_pred = []
	for document in corpus.documents:
		total_ok_doc = 0
		total_wrong_doc = 0
		# oov
		total_oov_ok_doc = 0
		total_oov_wrong_doc = 0
		for sentence in document.sentences:
			POS_refs = []
			forms = []
			for token in sentence.tokens:
				POS_refs.append(token.pos)
				forms.append(token.form)
			doc = Doc(nlp.vocab, words=forms, spaces = [True] * len(forms))
			doc = nlp(doc)
			pos_result = [tok.pos_ for tok in doc]
			form_result = [tok.text for tok in doc]
			is_oov = [tok.text not in vocab for tok in doc]
			total_ok_sent = 0
			total_wrong_sent = 0
			# oov
			total_oov_ok_sent = 0
			total_oov_wrong_sent = 0
			assert len(POS_refs) == len(pos_result)
			assert forms == form_result
			for pos_ref, pos_res, tok_is_oov in list(zip(POS_refs, pos_result, is_oov)):
				if pos_ref == pos_res:
					total_ok_sent += 1
					if tok_is_oov:
						total_oov_ok_sent += 1
				else:
					total_wrong_sent += 1
					if tok_is_oov:
						total_oov_wrong_sent += 1
				y_true.append(pos_ref)
				y_pred.append(pos_res)
			total_ok_doc += total_ok_sent
			total_wrong_doc += total_wrong_sent
			# oov
			total_oov_ok_doc += total_oov_ok_sent
			total_oov_wrong_doc += total_oov_wrong_sent
		total_ok_corpus += total_ok_doc
		total_wrong_corpus += total_wrong_doc
		# oov
		total_oov_ok_corpus += total_oov_ok_doc
		total_oov_wrong_corpus += total_oov_wrong_doc

	print("OK pos in the corpus:", total_ok_corpus)
	print("wrong pos in the corpus:", total_wrong_corpus)
	print("Accuracy corpus:", total_ok_corpus / (total_ok_corpus + total_wrong_corpus))

	# oov
	print("OK pos in the oov:", total_oov_ok_corpus)
	print("Wrong pos in the oov:", total_oov_wrong_corpus)
	print("Accuracy in the oov:", 0 if total_oov_ok_corpus == 0 else total_oov_ok_corpus / (total_oov_ok_corpus + total_oov_wrong_corpus))

	cf_matrix(y_true, y_pred)

import matplotlib.pyplot as plt
import seaborn as sns
def cf_matrix(y_true, y_pred):
	cf = confusion_matrix(y_true, y_pred)
	print(cf)

	plt.figure(figsize=(8, 6))
	sns.heatmap(cf, annot=True, cmap="Blues")
	plt.xlabel("Expected Labels", fontsize=14)
	plt.ylabel("Predicted Labels", fontsize=14)

	plt.show()

def main(file, model="fr_core_news_sm"):
	corpus = conll.conll_to_corpus(file)

	evaluate(corpus, model)

if __name__ == "__main__":
	file = sys.argv[1]
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--model', type=str, help="Spacy model to test", default="fr_core_news_sm")
	parser.add_argument('-c', '--corpus', type=str, help="conll file")

	args = parser.parse_args()
	main(args.corpus, args.model)
