#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt

time_start = time.time()
f = open("/home/w/data/Wiki-Vote.txt", "r")
G = nx.Graph()
for line in f:
    srcTar = line.strip().split()
    src = long(srcTar[0])
    tar = long(srcTar[1])
    G.add_edge(src, tar)
# G = nx.random_graphs.barabasi_albert_graph(100, 7)
P = 4
PLEN = len(G.edges)/P
VALL = len(G.nodes)
print len(G.edges), VALL

# x = list(G.nodes)[0]
# print x
# print list(G.neighbors(x))

# [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
Partitions = [[] for i in range(P)]
for i in range(P):
    core_set = set()
    boundary_set = set()
    while len(Partitions[i]) < PLEN:
        # nx.draw(G, node_color = 'b', edge_color = 'r', font_size = 18, node_size = 50)
        # plt.show()
        diff_set = boundary_set - core_set
        if len(diff_set) == 0:
            # print "aaaaaa"
            x = random.randint(0, len(G.edges)-1)  # 随机从当前剩余的图中选取一点作为起始点
            x = list(G.edges)[x][0]
        else:
            # print "bbbbbb"
            diff_list = list(diff_set)
            diff_neighbors = []
            for j in range(len(diff_list)):
                diff_neighbors.append(len(set(G.neighbors(diff_list[j])) - boundary_set))  # 选邻居数最小的作为候选点
            x = 0
            for j in range(len(diff_neighbors)):
                if diff_neighbors[j] < diff_neighbors[x]:
                    x = j
            x = diff_list[x]

        # print "x " ,x

        x_neighbors = list(set(G.neighbors(x)) - boundary_set)

        # print "x_neighbors " ,len(x_neighbors)

        core_set.add(x)
        boundary_set.add(x)
        for j in range(len(x_neighbors)):
            y = x_neighbors[j]
            boundary_set.add(y)
            y_neighbors = list(set(G.neighbors(y)) & boundary_set)
            for k in range(len(y_neighbors)):
                Partitions[i].append((y, y_neighbors[k]))
                G.remove_edge(y, y_neighbors[k])
                if len(Partitions[i]) > PLEN:
                    break
            if len(Partitions[i]) > PLEN:
                break
        # G.remove_node(x)

        # print "G.edges " ,len(G.edges)
        # print "\n"
        if len(G.edges) == 0:
            break
    if len(G.edges) == 0:
        break
# ans = 0
# for i in range(P):
#     print len(Partitions[i])
#     ans = ans + len(Partitions[i])
# print ans

Vertices = []
for i in range(P):
    v = set()
    for j in range(len(Partitions[i])):
        src = Partitions[i][j][0]
        tar = Partitions[i][j][1]
        v.add(src)
        v.add(tar)
    print len(v)
    Vertices.append(v)
for i in range(P):
    print len(Partitions[i])
VertexALL = 0
for i in range(len(Vertices)):
    VertexALL = VertexALL + len(Vertices[i])
VRF = VertexALL/1.0/VALL
print VRF




time_end = time.time()
time_used = time_end - time_start
print time_used
