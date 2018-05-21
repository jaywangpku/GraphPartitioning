#!/usr/bin/python
# -*- coding: utf-8 -*-

# 自己实现BFS代码，不采用调用库的形式，在进行BFS的过程中，将全部的边加上

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

time_start = time.time()

f = open("/home/w/data/testdata/test.txt", "w+")
g = nx.random_graphs.barabasi_albert_graph(100000 , 17)   # log2 n  100K nodes   (100000, 17)

a = list(g.edges())

print len(a)

# 源节点src对应的集合
srcvertex = set()  
# 每个源节点对应的tar组成的集合 
src2tar = {}

ans = []

for i in range(len(a)):
    srcvertex.add(a[i][0])
    if src2tar.has_key(a[i][0]):
        src2tar[a[i][0]].add(a[i][1])
    else:
        src2tar[a[i][0]] = set()
        src2tar[a[i][0]].add(a[i][1])


start = []
start.append(0)
i = 0
while(len(srcvertex)):
    if i > len(start) - 1:
        lsrcvertex = list(srcvertex)
        start.append(lsrcvertex[0])
        
    if src2tar.has_key(start[i]):
        for tar in src2tar[start[i]]:
            ans.append((start[i], tar))
            if tar not in start:
                start.append(tar)
        srcvertex.remove(start[i])
    print len(ans)
    i = i + 1

for i in range(len(ans)):
    temp = ans[i]
    src = str(temp[0])
    tar = str(temp[1])
    s = src + '\t' + tar + '\n'
    f.write(s)


time_end = time.time()
time_used = time_end - time_start

print time_used

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




