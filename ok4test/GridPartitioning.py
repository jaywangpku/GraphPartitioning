#!/usr/bin/python
# -*- coding: utf-8 -*-

# 完整的grid方案实现

import random
import math
import time

def GridAL(edgelist, numOfParts, rs, cs):
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # 存储总边数
    edgeNum = 0

    # grid 矩阵变量 做实验直接定义就可以了
    row = rs  # 行
    col = cs  # 列
    # { part:set(part1, part2,...),... }            初始化矩阵集合特性
    partSet = {}
    for i in range(0, numOfParts):
        tempSet = set()
        irow = int(i / col)
        icol = i - irow * col
        for j in range(0, numOfParts):
            jrow = int(j / col)
            jcol = j - jrow * col
            if irow == jrow:
                tempSet.add(j)
            if icol == jcol:
                tempSet.add(j)
        partSet[i] = tempSet
        del tempSet

    # 调试变量
    flag = 0

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
      
        mixingPrime = 1125899906842597L                          # 用于进行随机化，单纯使用 hash 会导致分配到的 part 很集中
        partsrc = abs(hash(src * mixingPrime)) % numOfParts
        parttar = abs(hash(tar * mixingPrime)) % numOfParts
        partset = partSet[partsrc] & partSet[parttar]
        partlist = list(partset)
        part = random.choice(partlist)

        # 更新各种集合数据
        Partitions[part].append((src, tar))
        
        # if vertexDic.has_key(part):
        #     vertexDic[part].add(src)
        #     vertexDic[part].add(tar)
        # else:
        #     vertexSet = set()  # 定义的是集合
        #     vertexSet.add(src)
        #     vertexSet.add(tar)
        #     vertexDic[part] = vertexSet

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
rs = [2, 3, 4, 6, 8, 10, 12, 14, 16]
for i in range(len(parts)):
    time_start = time.time()
    print parts[i]
    GridAL("/home/wj/swr/data/b-BFS.txt", parts[i], rs[i], rs[i])
    time_end = time.time()
    time_used = time_end - time_start
    print "time " + str(time_used)

# GridAL("/home/wj/swr/data/CC-Neuron_cci_changed.txt", 4, 2, 2)

# time_end = time.time()
# time_used = time_end - time_start
# print "time " + str(time_used)

