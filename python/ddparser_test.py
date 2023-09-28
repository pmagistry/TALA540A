#!/bin/python3
# -*- coding: utf-8 -*-


# pip3 install ddparser
# pip3 install paddlepaddle==2.4.2
# pip3 install LAC

# Télécharger le dossier zip sur github: https://github.com/baidu/DDParser
# le décompresser et aller au fichier setup.py

# pip3 install --force-reinstall paddlepaddle==2.4.2
# Utiliser cette version de paddlepaddle

# python3 setup.py install


from ddparser import DDParser
ddp = DDParser()
parsed = ddp.parse("百度是一家高科技公司")
print(parsed)

parsed = ddp.parse_seg([['百度', '是', '一家', '高科技', '公司'], ['他', '送', '了', '一本', '书']])
print(parsed)
