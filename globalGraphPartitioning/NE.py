#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt

f = open("/home/w/data/Wiki-Vote.txt", "r")
G = nx.DiGraph()
for line in f:
    srcTar = line.strip().split()
    src = long(srcTar[0])
    tar = long(srcTar[1])
    G.add_edge(src, tar)
P = 100
PLEN = len(G.edges)/100

# x = list(G.nodes)[0]
# print x
# print list(G.neighbors(x))

# [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
Partitions = [[] for i in range(P)]
for i in range(P):
	core_set = set()
	boundary_set = set()
	while len(Partitions[i]) < PLEN:
		diff_set = boundary_set - core_set
		if len(diff_set) == 0:
			print "aaaaaa"
			x = random.randint(0, len(G.nodes)-1)
			x = list(G.nodes)[x]
		else:
			print "bbbbbb"
			diff_list = list(diff_set)
			diff_neighbors = []
			for j in range(len(diff_list)):
				diff_neighbors.append(len(set(G.neighbors(diff_list[j])) - boundary_set))
			x = 0
			for j in range(len(diff_neighbors)):
				if diff_neighbors[j] < diff_neighbors[x]:
					x = j
			x = diff_list[x]

		print "x " ,x 

		x_neighbors = list(set(G.neighbors(x)) - boundary_set)

		print "x_neighbors " ,len(x_neighbors)

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
		print "G.edges " ,len(G.edges)

		print "\n"

for i in range(P):
	print len(Partitions[i])