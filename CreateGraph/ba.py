#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

g = nx.random_graphs.barabasi_albert_graph(100000, 17)   # log2 n  100K nodes


print g.nodes()
print g.edges()

# edges = list(BA.edges())
# print(len(edges))

# f = open("/home/w/data/testdata/ba-1.txt", "w")

# for i in range(len(edges)):
# 	temp = edges[i]
# 	src = str(temp[0])
# 	tar = str(temp[1])
# 	s = src + '\t' + tar + '\n'
# 	f.write(s)




