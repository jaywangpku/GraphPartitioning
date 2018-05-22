#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def Show(edgelist, numOfParts):
    f = open(edgelist, "r")
    # # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    # Partitions = [[] for i in range(numOfParts)]
    # # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    # vertexDic = {}
    # 存储总边数
    edgeNum = 0

    # 存储每个点的出入度
    verInDeg = {}
    verOutDeg = {}
    verDeg = {}
    
    for line in f:
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        
        edgeNum = edgeNum + 1
        if edgeNum % 1000000 == 0:
            print edgeNum

        # # 分边策略
        # part = random.randint(0, (int)(numOfParts - 1))
        
        # Partitions[part].append((src, tar))
        
        # if vertexDic.has_key(part):
        #     vertexDic[part].add(src)
        #     vertexDic[part].add(tar)
        # else:
        #     vertexSet = set()  # 定义的是集合
        #     vertexSet.add(src)
        #     vertexSet.add(tar)
        #     vertexDic[part] = vertexSet

        if verInDeg.has_key(tar):
            verInDeg[tar] = verInDeg[tar] + 1
        else:
            verInDeg[tar] = 1
        if verOutDeg.has_key(src):
            verOutDeg[src] = verOutDeg[src] + 1
        else:
            verOutDeg[src] = 1

    for ver in verOutDeg:
        verDeg[ver] = verOutDeg[ver]
    for ver in verInDeg:
        if verDeg.has_key(ver):
            verDeg[ver] = verDeg[ver] + verInDeg[ver]
        else:
            verDeg[ver] = verInDeg[ver]

    deg2num = {}
    maxDeg = 0

    for ver in verDeg:
        if verDeg[ver] > maxDeg:
            maxDeg = verDeg[ver]
    print "maxDeg" , maxDeg

    for i in range(0, maxDeg + 1):
         deg2num[i] = 0
    
    for ver in verDeg:
        deg2num[verDeg[ver]] = deg2num[verDeg[ver]] + 1

    deg_list = list(deg2num.keys())
    num_list = list(deg2num.values())

    i = 0
    while i < len(deg_list):
        if deg_list[i] > 0:
            deg_list[i] = math.log10(deg_list[i])
        if num_list[i] > 0:
            num_list[i] = math.log10(num_list[i])
        i = i + 1

    matplotlib.style.use('ggplot')
    plt.scatter(deg_list[1:], num_list[1:], marker = 'o', s = 5, color = 'blue', alpha = 0.3)
    # plt.title('Number of vertices and degrees')
    # plt.xlabel('The degrees')
    # plt.ylabel('The Numbers')
    plt.tight_layout()
    # plt.savefig('ans1.svg', dpi = 400)
    plt.show()



    # # 获取所有子图的顶点个数    
    # allVertex = 0L
    # maxVertices = 0L
    # for i in range(numOfParts):
    #     allVertex = allVertex + len(vertexDic[i])
    #     if maxVertices < len(vertexDic[i]):
    #         maxVertices = len(vertexDic[i])
    # # 获取整个图的顶点个数
    # vertexAll = vertexDic[0]
    # for i in range(1, numOfParts):
    #     vertexAll.update(vertexDic[i])
    # # 获取顶点的LSD和LRSD
    # temp = 0L
    # AveVerSize = len(vertexAll)/float(numOfParts)
    # for i in range(0, numOfParts):
    #     temp = temp + (len(vertexDic[i]) - AveVerSize) * (len(vertexDic[i]) - AveVerSize)
    # temp = temp/numOfParts
    # temp = math.sqrt(temp)

    # VLSD = temp
    # VLRSD = VLSD/AveVerSize

    # VRF = allVertex/float(len(vertexAll))
    
    # # 获取边的相关信息
    # maxEdges = 0L
    # AveSize = edgeNum/float(numOfParts)
    # temp = 0L
    # for i in range(numOfParts):
    #     temp = temp + (len(Partitions[i]) - AveSize) * (len(Partitions[i]) - AveSize)
    #     if maxEdges < len(Partitions[i]):
    #         maxEdges = len(Partitions[i])
    #     #print len(Partitions[i])
    # temp = temp/numOfParts
    # temp = math.sqrt(temp)

    # LSD = temp
    # LRSD = LSD/AveSize

    # # 依次是 VRF  LSD  LRSD  VLSD  VLRSD  子图点最大值  子图点平均值  子图边最大值  子图边平均值
    # print VRF, LSD, LRSD, VLSD, VLRSD, maxVertices, allVertex/numOfParts, maxEdges, edgeNum/numOfParts


    # for i in range(numOfParts):
    #     for j in range(len(Partitions[i])):
    #         print Partitions[i][j]
    #     print '\n'
   	


# time_start = time.time()

Show("/home/w/data/Wiki-Vote.txt", 100)

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

