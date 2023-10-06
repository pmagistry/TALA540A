#!/bin/python3

import spacy
from spacy.tokens import Doc
from spacy.tokenizer import Tokenizer
import conll
import re

from typing import Callable, Optional

"""
nlp = spacy.blank("fr")
words = ["Bonjour", "tout", "le", "monde", "!"]
spaces = [True for t in words]

doc = Doc(nlp.vocab, words=words, spaces=spaces)
print(doc.text)

print([(t.text, t.text_with_ws, t.whitespace_) for t in doc])
"""







#### Lecture du fichier conllu
#from conllu import parse

#sentences = parse(data)
#print(sentences)

FRENCH_MODELS=["fr_core_news_sm", "fr_core_news_md", "fr_core_news_lg", "fr_dep_news_trf"]
import fr_core_news_sm
#import fr_core_news_md
#import fr_core_news_lg
#import fr_dep_news_trf

def test_fichier_POS():
	header = conll.get_header("../data/fr_sequoia-ud-test.conllu")
	sentences = conll.get_sentences("../data/fr_sequoia-ud-test.conllu")

	# table of pandas DataFrames :'( :'(
	sentences = [conll.sentence_to_np(s, header) for s in sentences]
	#print(sentences[0])

	nlp = spacy.load(FRENCH_MODELS[0])
	nlp.tokenizer = Tokenizer(nlp.vocab, token_match=re.compile(r'\S+').match)
	#nlp = spacy.blank("fr")

	# test on every sentence
	total_ok = 0
	total_wrong = 0
	for sentence in sentences:
		tokens = sentence['FORM'].tolist()
		pos = sentence['UPOS'].tolist()
		print(tokens)
		print(pos)
		#doc = Doc(nlp.vocab, words=tokens)
		doc = nlp(' '.join(tokens))
		

		pos_result = [tok.pos_ for tok in doc]
		tok_result = [tok.text for tok in doc]
		print(tok_result)
		print(pos_result)

		total_ok_sent = 0
		total_wrong_sent = 0

		assert len(pos) == len(pos_result)
		for pos_label, pos_spacy in list(zip(pos, pos_result)):
			if pos_label == pos_spacy:
				total_ok_sent += 1
			else:
				total_wrong_sent += 1
		total_ok += total_ok_sent
		total_wrong += total_wrong_sent
		break
	print("OK pos:", total_ok)
	print("wrong pos:", total_wrong)
	print("Accuracy:", total_ok / (total_ok + total_wrong))

def main():
	test_fichier_POS()

if __name__ == "__main__":
	main()
