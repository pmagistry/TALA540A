#!/usr/bin/env python
# encoding : utf-8

from konlpy.tag import Kkma, Hannanum, Komoran, Mecab, Okt
import time

hannanum = Hannanum()
kkma=Kkma()
komoran = Komoran()
mecab = Mecab("/home/agathew/anaconda3/lib/python3.10/site-packages/mecab_ko_dic/dicdir/")
okt = Okt()

sentences="네, 안녕하세요. 반갑습니다. 질문이나 건의사항은 깃헙 이슈 트래커에 남겨주세요. 오류보고는 실행환경, 에러메세지와함께 설명을 최대한상세히!^^"

start=time.time()
print(f"Hannanum\n.analyse : {hannanum.analyze(sentences)}\n")
print(f"morphs : {hannanum.morphs(sentences)}\n")
print(f".nouns : {hannanum.nouns(sentences)}\n")
print(f".pos : {hannanum.pos(sentences)}\n")
end=time.time()
print(end-start, "\n\n")

start=end
print(f"Kkma\n{kkma.sentences(sentences)}\n")
print(f".morphs : {kkma.morphs(sentences)}\n")
print(f".nouns : {kkma.nouns(sentences)}\n")
print(f".pos : {kkma.pos(sentences)}\n")
end=time.time()
print(end-start, "\n\n")

start=end
print(f"Komoran\n.morphs : {komoran.morphs(sentences)}\n")
print(f".nouns : {komoran.nouns(sentences)}\n")
print(f".pos : {komoran.pos(sentences)}\n")
end=time.time()
print(end-start, "\n\n")

start=end
print(f"Mecab\n.morphs : {mecab.morphs(sentences)}\n")
print(f".nouns : {mecab.nouns(sentences)}\n")
print(f".pos : {mecab.pos(sentences)}\n")
end=time.time()
print(end-start, "\n\n")

start=end
print(f"Okt\n.phrases : {okt.phrases(sentences)}\n")
print(f".normalize : {okt.normalize(sentences)}\n")
print(f".nouns : {okt.nouns(sentences)}\n")
print(f".pos : {okt.pos(sentences)}\n")
end=time.time()
print(end-start, "\n\n")
