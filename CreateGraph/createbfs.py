#!/usr/bin/python
# -*- coding: utf-8 -*-

# 经证实，复杂度太高，不可行
# 构建边的bfs图

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from bidict import bidict

time_start = time.time()

f = open("/home/wj/swr/data/ba-bfs.txt", "w+")

g = nx.random_graphs.barabasi_albert_graph(100000, 17)   # log2 n  100K nodes   (100000, 17)
G = nx.Graph()

edges = list(g.edges())
nodes = list(g.nodes())

# 首先映射边集情况
edges_bd = bidict()
ed2no_bd = bidict()

print("1")

for i in range(len(edges)):
	if edges[i][0] > edges[i][1]:
		edges_bd[(edges[i][0], edges[i][1])] = (edges[i][1], edges[i][0])
		ed2no_bd[i] = (edges[i][1], edges[i][0])
	else:
		edges_bd[(edges[i][0], edges[i][1])] = (edges[i][0], edges[i][1])
		ed2no_bd[i] = (edges[i][0], edges[i][1])

ed2no_db = ed2no_bd.inv
edges_db = edges_bd.inv

print("2")

for i in range(len(edges)):
	G.add_node(i)


for i in range(len(nodes)):
	a = [n for n in g.neighbors(i)]
	e = []
	for j in range(len(a)):
		if i < a[j]:
			e.append(ed2no_db[(i,a[j])])
		else:
			e.append(ed2no_db[(a[j],i)])

	for m in range(len(e)):
		for mm in range(m+1,len(e)):
			G.add_edge(e[m], e[mm])

print("3")

b = list(nx.bfs_edges(G, 0))
c = []
for i in range(len(b)):
	if b[i][0] not in c:
		c.append(b[i][0])
	if b[i][1] not in c:
		c.append(b[i][1])

print("4")

# ans_edges = []
for i in range(len(c)):
	temp = edges_db[ed2no_bd[i]]
	src = str(temp[0])
	tar = str(temp[1])
	s = src + '\t' + tar + '\n'
	f.write(s)





# print ans_edges

# nx.draw(G)
# plt.show()

time_end = time.time()
time_used = time_end - time_start
print(time_used)
