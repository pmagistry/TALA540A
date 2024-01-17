#!/bin/python3
import sys

if len(sys.argv) != 2:
	print("usage: python convert_to_ud.py fichier.conllx")
	sys.exit(1)
in_file = sys.argv[1]

with open("ud_ctb_harbin.csv", 'r') as f:
	header = f.readline().strip()
	lines = f.readlines()

header = header.split(',')
UD_idx = header.index('UD')
CTB_idx = header.index('CTB')

correspondances = {}

for line in lines:
	line = line.split(',')
	UD = line[UD_idx]
	CTB = line[CTB_idx].split(':')
	for ctb in CTB:
		correspondances[ctb] = UD

UPOS_idx = 3
with open(in_file, 'r') as f:
	with open(in_file[:-1]+'u', 'w') as f2:
		for line in f.readlines():
			if line != "\n":
				line = line.split('\t')
				UPOS = line[UPOS_idx]
				UPOS = correspondances[UPOS]
				line[UPOS_idx] = UPOS
				line = '\t'.join(line)
			f2.write(line)
