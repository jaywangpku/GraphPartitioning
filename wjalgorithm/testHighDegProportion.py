#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import urllib
import random
import math
import time


f = open("/home/w/data/soc-LiveJournal1.txt","r")

vertexDic = {}  # {vertex:degree, ,,,}
edges = []

for line in f:
    srcTar = line.strip().split()
    src = long(srcTar[0])
    tar = long(srcTar[1])
    edges.append((src, tar))
    if vertexDic.has_key(src):
        vertexDic[src] = vertexDic[src] + 1
    else:
        vertexDic[src] = 1
    if vertexDic.has_key(tar):
        vertexDic[tar] = vertexDic[tar] + 1
    else:
        vertexDic[tar] = 1
print len(vertexDic)
# ans = []
# for i in range(2000):
#     ans.append(0)
# for key in vertexDic:
    # print str(key) + "   " + str(vertexDic[key])
#     ans[vertexDic[key]] += 1
# a = 0
# for i in range(501):
#     a += ans[i]
# print a, a/1.0/7115

# sortVertices = sorted(vertexDic.items(), key=lambda e:e[1], reverse = True)

# precent = 1
# Cut = len(sortVertices) / (100 / precent)
# BigestV = sortVertices[0:Cut]
# BigestVertex = []
# for i in range(Cut):
#     BigestVertex.append(BigestV[i][0])

# edgeNum = 0
# for i in range(len(edges)):
#     src = edges[i][0]
#     tar = edges[i][1]
#     if src in BigestVertex or tar in BigestVertex:
#         edgeNum = edgeNum + 1

# print edgeNum / 1.0 / len(edges)


