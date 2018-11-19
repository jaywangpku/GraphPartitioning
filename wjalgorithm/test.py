#!/usr/bin/python
# -*- coding: utf-8 -*-

# 自己实现BFS代码，不采用调用库的形式，在进行BFS的过程中，将全部的边加上
# 直接对边进行操作，在读取边的同时，将先被探索到的点在接下来的过程中其相关的边优先进行放置

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# time_start = time.time()

f = open("/home/w/data/Wiki-Vote.txt", "r")

# a = []

# for line in f:
#     srcTar = line.strip().split()
#     src = long(srcTar[0])
#     tar = long(srcTar[1])
#     a.append((src, tar))

# ans = {}
# for i in range(len(a)):
#     src = a[i][0]
#     tar = a[i][1]
#     if ans.has_key(src):
#         ans[src] = ans[src] + 1
#     else:
#         ans[src] = 1

# aa = 0
# for k,v in ans.items():
#     if ans[k] > aa:
#         aa = ans[k]
# print aa

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

# nx.draw(g)
# plt.show()


# edges = list(BA.edges())
# print(len(edges))

# f = open("/home/w/data/testdata/ba-1.txt", "w")

# for i in range(len(edges)):
#   temp = edges[i]
#   src = str(temp[0])
#   tar = str(temp[1])
#   s = src + '\t' + tar + '\n'
#   f.write(s)

edges = []
for i in range(100):
    edges.append(i)

edgesout = edges[0:30]

edgesset = set(edges)
edgesoutset = set(edgesout)
edges = list(edgesset-edgesoutset)
print edges[90]



