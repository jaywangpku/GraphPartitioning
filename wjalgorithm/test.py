#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def SimpleBufAL(edgelist, numOfParts):
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # { vertex:set(part1, part2,...),... }          存储每个点对应的分区
    ver2partDic = {}
    
    # { vertex:degree,... }                         存储每个点对应的度信息
    ver2degreeDic = {}
    # {(src, tar):balance, ...}                     存储buf中每条边的平衡度
    edgeBalance = {}

    # 存储总边数
    edgeNum = 0

    # 将边转换为标准形式，存储在lines中
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        lines[i] = (src, tar)

    vertexOut = {}
    vertexIn = {}
    vertex = []

    for i in range(len(lines)):
        src = lines[i][0]
        tar = lines[i][1]
        if vertexOut.has_key(src):
            vertexOut[src] = vertexOut[src] + 1
        else:
            vertexOut[src] = 1
        if vertexIn.has_key(tar):
            vertexIn[tar] = vertexIn[tar] + 1
        else:
            vertexIn[tar] = 1
        if src not in vertex:
            vertex.append(src)
        if tar not in vertex:
            vertex.append(tar)

    for i in range(len(vertex)):
        if vertexIn.has_key(vertex[i]):
            indeg = vertexIn[vertex[i]]
        else:
            indeg = 0
        if vertexOut.has_key(vertex[i]):
            outdeg = vertexOut[vertex[i]]
        else:
            outdeg = 0
        print indeg, outdeg


SimpleBufAL("/home/w/data/soc-pokec-relationships.txt", 100)

