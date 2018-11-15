#!/usr/bin/python
# -*- coding: utf-8 -*-

# 该算法用于创建不同的度分布的图

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from bidict import bidict


nodes = 10000000
maxdeg = 25000

zeta = 1.341
s = []
for i in range(1, maxdeg):
	j = np.power(1.0/i, 2.5)
	j = int(j * nodes)
	for k in range(j):
		s.append(i)
random.shuffle(s)
ss = s[0:1000]
print ss

sequence = ss
G = nx.random_degree_sequence_graph(sequence)
edges = G.edges()
print edges
# nx.draw(G, pos=nx.spring_layout(G), node_color = 'r', edge_color = 'b', with_labels = True, font_size = 1, node_size = 100)
# plt.show()