#!/bin/python3
# -*- coding: utf-8 -*-

import sys

from corpus import Corpus, Document, Sentence, Token

def conll_to_corpus(file: str) -> Corpus:
	file = open(file, 'r')
	data = file.read()  # raw string
	file.close()

	sentences = "\n".join([s[9:] for s in data.split("\n") if s.startswith("# text")])
	# each line that starts with # text

	tokens_string = "\n".join([s for s in data.split("\n") if not s.startswith("#")])
	# each line that does not start with #

	sent_tokens = tokens_string.split("\n\n")
	sent_string = sentences.split("\n")

	s = [] # list of Sentence objects

	# Gets POS from sent_tokens for each sentence
	for sentence, tokens in list(zip(sent_string, sent_tokens)):
		t = []
		for token_line in tokens.split('\n'):
			token_line = token_line.split('\t')
			if len(token_line) < 10:
				continue
			form = token_line[1]
			lemma = token_line[2]
			upos = token_line[3]
			xpos = token_line[4]
			feats = token_line[5]
			head = token_line[6]
			deprel = token_line[7]
			deps = token_line[8]
			misc = token_line[9]
			t.append(Token(form, lemma, upos))
			
		s.append(Sentence(sentence, t))
	d = Document(s)
	c = Corpus([d]) # only one document
	return c

def main(file):
	corpus = conll_to_corpus(file)
	print(corpus.documents[0].sentences[0].sentence)

if __name__ == "__main__":
	args = sys.argv	
	if len(args) < 2:
		print("Use: conll.py file.conll")
		sys.exit(1)
	main(args[1])
