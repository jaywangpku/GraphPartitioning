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

    # 缓冲区大小控制
    bufs = 100            # 缓冲区总大小
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

        # 计算每一条边对应的平衡度
        # edgeBalance = {}
        # for i in range(len(edgeBuf)):
        #     difference = ver2degreeDic[edgeBuf[i][0]] - ver2degreeDic[edgeBuf[i][1]]
        #     summation = ver2degreeDic[edgeBuf[i][0]] + ver2degreeDic[edgeBuf[i][1]]
        #     balance = abs(difference) / 1.0 / summation
        #     edgeBalance[edgeBuf[i]] = balance
        
        # edge = edgeBuf[0]
        # for i in range(len(edgeBuf)):
        #     if edgeBalance[edge] < edgeBalance[edgeBuf[i]]:
        #         edge = edgeBuf[i]

        edgesocre = {}
        for i in range(len(edgeBuf)):
            summation = ver2degreeDic[edgeBuf[i][0]] + ver2degreeDic[edgeBuf[i][1]]
            edgesocre[edgeBuf[i]] = summation

        edge = edgeBuf[0]
        for i in range(len(edgeBuf)):
            if edgesocre[edge] > edgesocre[edgeBuf[i]]:
                edge = edgeBuf[i]

        edgeBuf.remove(edge)
        # print len(edgeBuf)

        # 将选出来的边进行和分配
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

        if (len(srcMachines) == 0) and (len(tarMachines) == 0):      # A(u) 和 A(v) 都是空集  选择边数量最少的子图加入
            part = -1
            for i in range(numOfParts):
                if part == -1:
                    part = i
                    continue 
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif (len(srcMachines) > 0) and (len(tarMachines) == 0):
            part = -1
            for i in srcMachines:
                if part == -1:
                    part = i
                    continue
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif (len(srcMachines) == 0) and (len(tarMachines) > 0):
            part = -1
            for i in tarMachines:
                if part == -1:
                    part = i
                    continue
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif ((len(srcMachines) > 0) and len(tarMachines) > 0):
            Intersection = srcMachines & tarMachines
            Convergence = srcMachines | tarMachines
            if (len(Intersection) > 0):
                part = -1
                for i in Intersection:
                    if part == -1:
                        part = i
                        continue
                    if len(Partitions[i]) < len(Partitions[part]):
                        part = i
            elif (len(Intersection) == 0):
                part = -1
                for i in Convergence:
                    if part == -1:
                        part = i
                        continue
                    if len(Partitions[i]) < len(Partitions[part]):
                        part = i


        # 如果是最后一个阶段
        # elif edgefileOver == 1:
        #     print "最后阶段"

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
SimpleBufAL("/home/w/data/Wiki-VoteRandom.txt", 100)

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

