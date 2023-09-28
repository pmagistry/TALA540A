#!/bin/python3
#coding=utf-8

# pip install deepnlp



from __future__ import unicode_literals
import deepnlp

"""
deepnlp.download('segment')
deepnlp.download('pos')
deepnlp.download('ner')
deepnlp.download('parse')
"""

from deepnlp import segmenter
# Problems:
#     import CRFPP
#ModuleNotFoundError: No module named 'CRFPP'

# Solution:
# sudo apt-add-repository 'deb http://cl.naist.jp/~eric-n/ubuntu-nlp oneiric all'
# sudo apt-get update
# sudo apt-get install libcrf++-dev crf++

def main():
	print("Hello")

if __name__ == "__main__":
	main()
