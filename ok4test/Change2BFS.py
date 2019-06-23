import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import urllib
import math
import time
import random
import networkx as nx

G = nx.Graph()
f = open("C:/Users/user/Desktop/datasets/soc-LiveJournal1.txt","r")
for line in f:
    srcTar = line.strip().split()
    if(srcTar[0]=='#'):
        continue
    src = long(srcTar[0])
    tar = long(srcTar[1])
    G.add_edge(src,tar)

f.close()
c = list(nx.algorithms.coloring.strategy_connected_sequential_bfs(G, 0))
cc = {}
for i in range(len(c)):
    cc[c[i]] = i

sortedlist = sorted(edges, key = lambda x: (cc[x[0]], cc[x[1]]))
fn = open("C:/Users/user/Desktop/datasets/soc-LiveJournal1-BFS.txt","w+")
for i in range(len(sortedlist)):
    s = str(sortedlist[i][0]) + '\t' + str(sortedlist[i][1]) + '\n'
    fn.write(s)

fn.close()