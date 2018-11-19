#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def Show(edgelist, numOfParts):
    f = open(edgelist, "r")
    ftar = open("/home/w/data/Wiki-Vote-DFS1.txt", "w+")

    g = nx.DiGraph()
    edgeNum = 0
    edges = 0
    v = 0
    ans = []

    for line in f:
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        
        edgeNum = edgeNum + 1
        if edgeNum % 1000000 == 0:
            print edgeNum

        g.add_edge(src, tar)

    # nx.draw(g)

    # while(len(g)):
        # nx.draw(g)
        # plt.show()
    
    b = list(g.edges())
    while(len(b)):

        v = b[0][0]
        a = list(nx.dfs_edges(g, source = v))
        
        edges = edges + len(a)
        print edges

        for i in range(len(a)):
            src = a[i][0]
            tar = a[i][1]
            s = str(src) + '\t' + str(tar) + '\n'
            ftar.write(s)

        
        b = list(set(b) - set(a))
        # print ans
        g.remove_edges_from(a)   
        a = []
        

    
    # print edgeNum, edges
    
    # for i in range(len(ans)):
    #     src = a[i][0]
    #     tar = a[i][1]
    #     print src, tar

    # plt.show()
    

time_start = time.time()

Show("/home/w/data/Wiki-Vote.txt", 100)

# Wiki-Vote.txt   soc-pokec-relationships.txt   soc-LiveJournal1.txt   mytest.txt


time_end = time.time()
time_used = time_end - time_start

print time_used
