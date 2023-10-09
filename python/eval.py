#!/bin/python3
# -*- coding: utf-8 -*-

import corpus, conll
import argparse
import sys
import re

from spacy.tokens import Doc

def import_spacy(model):
	# Spacy imports
	import spacy
	from spacy.tokenizer import Tokenizer

	module = __import__(model, fromlist=[model])
	#Model = getattr(module)
	#print(model)
	#model_class = eval(model)
	#import model_class
	nlp = spacy.load(model)
	#nlp.tokenizer = Tokenizer(nlp.vocab, token_match=re.compile(r'\S+').match)
	return nlp

def evaluate(corpus, model):
	# import model from spacy
	nlp = import_spacy(model)
	total_ok_corpus = 0
	total_wrong_corpus = 0
	for document in corpus.documents:
		total_ok_doc = 0
		total_wrong_doc = 0
		for sentence in document.sentences:
			POS_refs = []
			forms = []
			for token in sentence.tokens:
				POS_refs.append(token.pos)
				forms.append(token.form)
			#doc = nlp(' '.join(forms))
			doc = Doc(nlp.vocab, words=forms, spaces = [True] * len(forms))
			doc = nlp(doc)
			pos_result = [tok.pos_ for tok in doc]
			form_result = [tok.text for tok in doc]
			total_ok_sent = 0
			total_wrong_sent = 0
			assert len(POS_refs) == len(pos_result)
			for pos_ref, pos_res in list(zip(POS_refs, pos_result)):
				if pos_ref == pos_res:
					total_ok_sent += 1
				else:
					total_wrong_sent += 1
			total_ok_doc += total_ok_sent
			total_wrong_doc += total_wrong_sent
		total_ok_corpus += total_ok_doc
		total_wrong_corpus += total_wrong_doc

	print("OK pos in the corpus:", total_ok_corpus)
	print("wrong pos in the corpus:", total_wrong_corpus)
	print("Accuracy corpus:", total_ok_corpus / (total_ok_corpus + total_wrong_corpus))


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
