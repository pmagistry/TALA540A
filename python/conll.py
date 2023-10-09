#!/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import sys

from io import StringIO
from corpus import Corpus, Document, Sentence, Token
from typing import List

def get_sentences(file: str) -> list:
	file = open(file, "r")
	data = file.read()
	file.close()

	sentences = "\n".join([s for s in data.split("\n") if not s.startswith("#")])
	sentences = sentences.split("\n\n")
	
	return sentences

def get_header(file: str) -> list:
	file = open(file, "r")
	line = file.readline()
	while not line.startswith("# global.columns"):
		line = file.readline()
	line = line.split('=')[1].split(' ')[1:]
	return line

def sentence_to_np(sentence: str, head: list):
	#csvStringIO = StringIO(sentence)
	#df = pd.read_csv(csvStringIO, sep='\t')	
	#df = pd.read_csv(sentence)	
	table = []
	for line in sentence.split("\n"):
		line_table = []
		for field in line.split("\t"):
			line_table.append(field)
		table.append(line_table)

	try:
		df = pd.DataFrame(table, columns=head)
		return df
	except:
		print("ERROR ON THIS TABLE:")
		print(table)
		print("FORMAT MISMATCH FOR HEADER:")
		print(head)

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
	"""
	print(sent_tokens[0])
	print(sent_string[0])
	"""

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
