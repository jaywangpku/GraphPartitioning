#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

time_start = time.time()


g = nx.random_graphs.barabasi_albert_graph(100000 * 20, 21)   # log2 n  100K nodes   (100000, 17)


a = list(nx.bfs_edges(g, 1))


time_end = time.time()
time_used = time_end - time_start

print time_used

# nx.draw(g)
# plt.show()


# edges = list(BA.edges())
# print(len(edges))

# f = open("/home/w/data/testdata/ba-1.txt", "w")

# for i in range(len(edges)):
# 	temp = edges[i]
# 	src = str(temp[0])
# 	tar = str(temp[1])
# 	s = src + '\t' + tar + '\n'
# 	f.write(s)




