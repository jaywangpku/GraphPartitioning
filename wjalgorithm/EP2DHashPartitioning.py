#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time

def EP2DhashAL(edgelist, numOfParts):
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # 存储总边数
    edgeNum = 0
    
    for line in f:
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        
        edgeNum = edgeNum + 1
        if edgeNum % 1000000 == 0:
            print edgeNum

        # 分边策略
        mixingPrime = 1125899906842597L                          # 用于进行随机化，单纯使用 hash 会导致分配到的 part 很集中
        ceilSqrtNumParts = int(math.ceil(math.sqrt(numOfParts)))
        col = abs(src * mixingPrime) % ceilSqrtNumParts
        row = abs(tar * mixingPrime) % ceilSqrtNumParts
        part = abs(col * ceilSqrtNumParts + row) % numOfParts

        # 这个设计方案有问题，可以详细思考为什么会出现这种情况  ??????

        # mixingPrime = 1125899906842597L
        # #parId = int(abs(src * mixingPrime) % numOfPar)
        # ceilSqrtNumParts = int(math.ceil(math.sqrt(numOfParts)))
        # part = -1
        # if(numOfParts == ceilSqrtNumParts * ceilSqrtNumParts):
        #     col = int(abs(src * mixingPrime) % numOfParts)
        #     row = int(abs(tar * mixingPrime) % numOfParts)
        #     part = (col * ceilSqrtNumParts + row) % numOfParts
        # else:
        #     cols = ceilSqrtNumParts
        #     rows = (numOfParts + cols - 1) / cols
        #     lastColRows = numOfPar - rows * (cols - 1)
        #     col = int(abs(src * mixingPrime) % numOfParts / rows)
        #     row = -1
        #     if col < cols -1:
        #         row = int(abs(tar * mixingPrime) % rows)
        #     else:
        #         row = int(abs(tar * mixingPrime) % lastColRows)
        #     part = col * rows + row
        
        Partitions[part].append((src, tar))
        
        if vertexDic.has_key(part):
            vertexDic[part].add(src)
            vertexDic[part].add(tar)
        else:
            vertexSet = set()  # 定义的是集合
            vertexSet.add(src)
            vertexSet.add(tar)
            vertexDic[part] = vertexSet
    
    # 获取所有子图的顶点个数    
    allVertex = 0L
    maxVertices = 0L
    for i in range(numOfParts):
        allVertex = allVertex + len(vertexDic[i])
        if maxVertices < len(vertexDic[i]):
            maxVertices = len(vertexDic[i])
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
    AveSize = edgeNum/float(numOfParts)
    temp = 0L
    for i in range(numOfParts):
        temp = temp + (len(Partitions[i]) - AveSize) * (len(Partitions[i]) - AveSize)
        if maxEdges < len(Partitions[i]):
            maxEdges = len(Partitions[i])
        #print len(Partitions[i])
    temp = temp/numOfParts
    temp = math.sqrt(temp)

    LSD = temp
    LRSD = LSD/AveSize

    # 依次是 VRF  LSD  LRSD  VLSD  VLRSD  子图点最大值  子图点平均值  子图边最大值  子图边平均值
    print VRF, LSD, LRSD, VLSD, VLRSD, maxVertices, allVertex/numOfParts, maxEdges, edgeNum/numOfParts


    # for i in range(numOfParts):
    #     for j in range(len(Partitions[i])):
    #         print Partitions[i][j]
    #     print '\n'


# time_start = time.time()

# EP2DhashAL("/home/w/data/Wiki-Vote.txt", 100)

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

