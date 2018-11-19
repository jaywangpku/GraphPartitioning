import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

g = nx.Graph()

f = open("/home/w/data/mytest.txt", "r")

for line in f:
    srcTar = line.strip().split()
    src = long(srcTar[0])
    tar = long(srcTar[1])

    g.add_edge(src, tar)


print len(g.nodes())

a = list(nx.bfs_edges(g, 1))

print len(a)

nx.draw(g)
plt.show()

