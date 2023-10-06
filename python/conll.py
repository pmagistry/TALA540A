#!/bin/python3

import numpy as np
import pandas as pd

from io import StringIO

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
