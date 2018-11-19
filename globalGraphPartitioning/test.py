#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt

# G = nx.random_graphs.barabasi_albert_graph(20, 4)	# 生成的是无向图
# G = nx.DiGraph()
# G.add_edge(1, 2)
# G.add_edge(2, 3)

# print len(G.edges)

# print len(list(G.neighbors(2)))
# nx.draw(G, node_color = 'b', edge_color = 'r', font_size = 18, node_size = 50)
# plt.show()


# 将图改成无向图
# f = open("/home/w/data/Wiki-Vote.txt", "r")
# f1 = open("/home/w/data/Wiki-Vote-undirected.txt", "w+")
# G = nx.Graph()
# for line in f:
#     srcTar = line.strip().split()
#     src = long(srcTar[0])
#     tar = long(srcTar[1])
#     G.add_edge(src, tar)
# edges = list(G.edges)
# for i in range(len(edges)):
# 	src = edges[i][0]
# 	tar = edges[i][1]
# 	s = str(src) + "\t" + str(tar) + "\n"
# 	f1.write(s)