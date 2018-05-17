#!/usr/bin/python
# -*- coding: utf-8 -*-

# 构建边的bfs图

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

time_start = time.time()


g = nx.random_graphs.barabasi_albert_graph(100, 7)   # log2 n  100K nodes   (100000, 17)
G = nx.Graph()

edges = list(g.edges())
nodes = list(g.nodes())

for i in range(len(edges)):
	G.add_node(i)



for i in range(len(nodes)):
	a = [n for n in g.neighbors(i)]
	print a






a = list(nx.bfs_edges(g, 1))





# nx.draw(G)
# plt.show()






time_end = time.time()
time_used = time_end - time_start
print time_used
