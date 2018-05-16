#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx

BA = nx.random_graphs.barabasi_albert_graph(10000, 13)   # log2 n

# print BA.nodes()
# print BA.edges()

edges = list(BA.edges())
print(len(edges))

f = open("ba-10000.txt", "w")

for i in range(len(edges)):
	temp = edges[i]
	src = str(temp[0])
	tar = str(temp[1])
	s = src + '\t' + tar + '\n'
	f.write(s)



