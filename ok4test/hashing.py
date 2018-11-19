#!/usr/bin/python
# -*- coding: utf-8 -*-

# 完整的hashing方案实现

import random
import math
import time

def hashing(edgelist, numOfParts):
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # 存储总边数
    edgeNum = 0

    for i in range(numOfParts):
        vertexDic[i] = set()
    
    for line in f:
        srcTar = line.strip().split()
        if(srcTar[0] == '#'):
            continue
        src = long(srcTar[0])
        tar = long(srcTar[1])
        
        edgeNum = edgeNum + 1
        if edgeNum % 1000000 == 0:
            print edgeNum

        # 分边策略
        mixingPrime = 1125899906842597L
        part = abs(hash(src * mixingPrime + tar)) % numOfParts
        
        Partitions[part].append((src, tar))
        
        vertexDic[part].add(src)
        vertexDic[part].add(tar)
        

    # 获取所有子图的顶点个数    
    allVertex = 0L
    maxVertices = 0L
    minVertices = 1000000000L
    for i in range(numOfParts):
        allVertex = allVertex + len(vertexDic[i])
        print len(vertexDic[i])
        if maxVertices < len(vertexDic[i]):
            maxVertices = len(vertexDic[i])
        if minVertices > len(vertexDic[i]):
            minVertices = len(vertexDic[i])
    # 获取整个图的顶点个数
    vertexAll = vertexDic[0]
    for i in range(1, numOfParts):
        vertexAll.update(vertexDic[i])
    # 获取顶点的LSD和LRSD
    temp = 0L
    AveVerSize = len(vertexAll)/float(numOfParts)
    for i in range(0, numOfParts):
        temp = temp + (len(vertexDic[i]) - AveVerSize) * (len(vertexDic[i]) - AveVerSize)
    temp = temp/numOfParts
    temp = math.sqrt(temp)

    VLSD = temp
    VLRSD = VLSD/AveVerSize

    VRF = allVertex/float(len(vertexAll))
    
    # 获取边的相关信息
    maxEdges = 0L
    minEdges = 1000000000L
    AveSize = edgeNum/float(numOfParts)
    temp = 0L
    for i in range(numOfParts):
        temp = temp + (len(Partitions[i]) - AveSize) * (len(Partitions[i]) - AveSize)
        if maxEdges < len(Partitions[i]):
            maxEdges = len(Partitions[i])
        if minEdges > len(Partitions[i]):
            minEdges = len(Partitions[i])
        print len(Partitions[i])
    temp = temp/numOfParts
    temp = math.sqrt(temp)

    LSD = temp
    LRSD = LSD/AveSize

    # 依次是 VRF  LSD  LRSD  VLSD  VLRSD  子图点最大值  子图点平均值  子图边最大值  子图边平均值
    # print VRF, LSD, LRSD, VLSD, VLRSD, maxVertices, allVertex/numOfParts, maxEdges, edgeNum/numOfParts
    print "VRF " + str(VRF)
    print "max-edges " + str(maxEdges)
    print "min-edges " + str(minEdges)
    print "avg-edges " + str(edgeNum/numOfParts)
    print "max-vertices " + str(maxVertices)
    print "min-vertices " + str(minVertices)
    print "avg-vertices " + str(allVertex/numOfParts)
    print "LRSD " + str(LRSD)
    print "VLRSD " + str(VLRSD)

    # for i in range(numOfParts):
    #     for j in range(len(Partitions[i])):
    #         print Partitions[i][j]
    #     print '\n'


# time_start = time.time()

parts = [4, 9, 16, 36, 64, 100, 144, 196, 256]
for i in range(len(parts)):
    time_start = time.time()
    print parts[i]
    hashing("/home/wj/swr/data/cit-Patents.txt", parts[i])
    time_end = time.time()
    time_used = time_end - time_start
    print "time " + str(time_used)

# hashing("/home/wj/swr/data/user_sns.txt", 256)

# time_end = time.time()
# time_used = time_end - time_start
# print "time " + str(time_used)
