#!/bin/python3
#coding:utf-8

import torch
from ltp import LTP

ltp = LTP("LTP/small")

if torch.cuda.is_available():
	ltp.to("cuda")

#  分词 cws、词性 pos、命名实体标注 ner、语义角色标注 srl、依存句法分析 dep、语义依存分析树 sdp、语义依存分析图 sdpg
output = ltp.pipeline(["他叫汤姆去拿外衣。"], tasks=["cws", "pos", "ner", "srl", "dep", "sdp", "sdpg"])


print(output.cws)  # print(output[0]) / print(output['cws']) # 也可以使用下标访问
print(output.pos)
print(output.sdp)













# 使用感知机算法实现的分词、词性和命名实体识别，速度比较快，但是精度略低
ltp = LTP("LTP/legacy")
# cws, pos, ner = ltp.pipeline(["他叫汤姆去拿外衣。"], tasks=["cws", "ner"]).to_tuple() # error: NER 需要 词性标注任务的结果
cws, pos, ner = ltp.pipeline(["他叫汤姆去拿外衣。"], tasks=["cws", "pos", "ner"]).to_tuple()  # to tuple 可以自动转换为元组格式
# 使用元组格式作为返回结果
print(cws, pos, ner)
