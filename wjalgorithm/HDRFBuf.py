#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def HDRFBufAL(edgelist, numOfParts):
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

    # { part1:score, part2:score,... }              存储每一条边相对每个子图的分数
    partSocre2edge = {}

    x = 1.2

    # 存储总边数
    edgeNum = 0

    # 缓冲区大小控制
    bufs = 10             # 缓冲区总大小
    buf = 1               # 每次填充的数量
    edgeBuf = []
    vertexBuf = set()

    # 状态标记变量
    edgefileOver = -1     # -1 表示初始填充阶段  0 表示中期循环阶段  1 表示最后处理阶段
    
    # 调试变量
    flag = 0

    # 进行各种初始化操作
    for i in range(numOfParts):
        vertexDic[i] = set()

    # 将边转换为标准形式，存储在lines中
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        lines[i] = (src, tar)

        # edgeNum = edgeNum + 1
        # if edgeNum % 1000000 == 0:
        #     print edgeNum
    line = bufs
    while edgefileOver < 2:
        if edgefileOver == -1: 
            edgeBuf = lines[0:bufs]
            for i in range(bufs):
                src = edgeBuf[i][0]
                tar = edgeBuf[i][1]
                if ver2degreeDic.has_key(src):
                    ver2degreeDic[src] = ver2degreeDic[src] + 1
                else:
                    ver2degreeDic[src] = 1
                if ver2degreeDic.has_key(tar):
                    ver2degreeDic[tar] = ver2degreeDic[tar] + 1
                else:
                    ver2degreeDic[tar] = 1
            edgefileOver = 0
        elif edgefileOver == 0:
            for i in range(buf):
                edgeBuf.append(lines[line])
                src = lines[line][0]
                tar = lines[line][1]
                if ver2degreeDic.has_key(src):
                    ver2degreeDic[src] = ver2degreeDic[src] + 1
                else:
                    ver2degreeDic[src] = 1
                if ver2degreeDic.has_key(tar):
                    ver2degreeDic[tar] = ver2degreeDic[tar] + 1
                else:
                    ver2degreeDic[tar] = 1
                if line == len(lines) - 1:
                    edgefileOver = 1
                    break
                line = line + 1
        elif edgefileOver == 1:
            if len(edgeBuf) == 0:
                break

        # 构建缓冲区子图
        # g = nx.Graph()
        # for i in range(bufs):
        #     g.add_edge(edgeBuf[i][0], edgeBuf[i][1])
        # nx.draw(g, node_size = 20, node_color = 'r')
        # plt.show()

        maxsize = 0
        minsize = 100000000
        for i in range(numOfParts):
            if maxsize < len(Partitions[i]):
                maxsize = len(Partitions[i])
            if minsize > len(Partitions[i]):
                minsize = len(Partitions[i])

        maxdeg = 0
        for i in range(len(edgeBuf)):
            src = edgeBuf[i][0]
            tar = edgeBuf[i][1]
            if maxdeg < ver2degreeDic[src]:
                maxdeg = ver2degreeDic[src]
            if maxdeg < ver2degreeDic[tar]:
                maxdeg = ver2degreeDic[tar]


        # 计算每一条边对应的平衡度
        # edgeBalance = {}
        # for i in range(len(edgeBuf)):
        #     srcdeg = ver2degreeDic[edgeBuf[i][0]]
        #     tardeg = ver2degreeDic[edgeBuf[i][1]]
        #     difference = ver2degreeDic[edgeBuf[i][0]] - ver2degreeDic[edgeBuf[i][1]]
        #     summation = ver2degreeDic[edgeBuf[i][0]] + ver2degreeDic[edgeBuf[i][1]]
        #     balance = abs(difference) / 1.0 / summation
        #     edgeBalance[edgeBuf[i]] = balance
        
        # edge = edgeBuf[0]
        # for i in range(len(edgeBuf)):
        #     if edgeBalance[edge] < edgeBalance[edgeBuf[i]]:
        #         edge = edgeBuf[i]

        # edgeBuf.remove(edge)
        # print len(edgeBuf)

        # 将选出来的边进行和分配
        bigsocre = {}
        for i in range(len(edgeBuf)):
            # 记录每一条边对应每一个子图的socre
            edge = edgeBuf[i]
            src = edge[0]
            tar = edge[1]
            if ver2partDic.has_key(src):
                srcMachines = ver2partDic[src]
            else:
                src2partSet = set()
                ver2partDic[src] = src2partSet
                srcMachines = ver2partDic[src]

            if ver2partDic.has_key(tar):
                tarMachines = ver2partDic[tar]
            else:
                tar2partSet = set()
                ver2partDic[tar] = tar2partSet
                tarMachines = ver2partDic[tar]

            for partTemp in range(numOfParts):

                if ver2degreeDic.has_key(src):
                    partialDegSrc = ver2degreeDic[src]
                else:
                    partialDegSrc = 0
                    ver2degreeDic[src] = partialDegSrc

                if ver2degreeDic.has_key(tar):
                    partialDegTar = ver2degreeDic[tar]
                else:
                    partialDegTar = 0
                    ver2degreeDic[tar] = partialDegTar

                if partialDegSrc == 0 and partialDegTar == 0:
                    rDegSrc = 0
                    rDegTar = 0
                else:
                    rDegSrc = partialDegSrc / (float)(partialDegSrc + partialDegTar)
                    rDegTar = partialDegTar / (float)(partialDegSrc + partialDegTar)
                    # rDegSrc = partialDegSrc / 2.0 / maxdeg
                    # rDegTar = partialDegTar / 2.0 / maxdeg

                if partTemp in srcMachines:
                    gsrc = 1 + (1 - rDegSrc)
                else:
                    gsrc = 0
                if partTemp in tarMachines:
                    gtar = 1 + (1 - rDegTar)
                else:
                    gtar = 0

                rep = gsrc + gtar

                bal = x * (maxsize - len(Partitions[partTemp])) / (float)(maxsize - minsize + 1)   # 加 1 避免除 0

                score = rep + bal #+ edgeBalance[edgeBuf[i]]

                partSocre2edge[partTemp] = score
                bigsocre[(i,partTemp)] = score


        e = 0 
        part = 0
        for key, value in bigsocre.items():
            if bigsocre[(e, part)] <= bigsocre[(key)]:
                e = key[0]
                part = key[1]
        print e, part

        src = edgeBuf[e][0]
        tar = edgeBuf[e][1]
        edgeBuf.remove((src, tar))
        # for j in range(numOfParts):
        #     if partSocre2edge[part] < partSocre2edge[j]:
        #         part = j

        # 更新各种集合数据
        Partitions[part].append((src, tar))

        vertexDic[part].add(src)
        vertexDic[part].add(tar)

        ver2partDic[src].add(part)
        ver2partDic[tar].add(part)

    # 对分配信息进行统计
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
    # AveSize = edgeNum/float(numOfParts)
    AveSize = len(lines)/float(numOfParts)
    temp = 0L
    for i in range(numOfParts):
        temp = temp + (len(Partitions[i]) - AveSize) * (len(Partitions[i]) - AveSize)
        if maxEdges < len(Partitions[i]):
            maxEdges = len(Partitions[i])
        print len(Partitions[i])
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

# wjAL("/home/w/data/Wiki-VoteRandom.txt", 20)
# HDRFBufAL("/home/w/data/rmat/Armat-10000.txt", 100)
HDRFBufAL("/home/w/data/Wiki-Vote.txt", 100)


# time_end = time.time()
# time_used = time_end - time_start

# print time_used

