#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time

def singleWindowGreedy(edgelist, numOfParts):
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # { vertex:set(part1, part2,...),... }          存储每个点对应的分区
    ver2partDic = {}
    # { vertex:degree,... }                         存储每个点对应的度信息
    ver2degreeDic = {}
    # { part1:score, part2:score,... }              存储每一条边相对每个子图的分数
    partSocre2edge = {}
    # 存储总边数
    edgeNum = 0
    # 存储全部的边集
    Edgeall = []

    # 单滑动窗口大小
    window = 10000             # 103689  Wiki-Vote
    win = []
    winedges = 0

    # 文中所给的 lamda 参数
    x = 1.0

    # 调试变量
    flag = 0

    for i in range(numOfParts):
        vertexDic[i] = set()

    for line in f:
        Edgeall.append(line.strip().split())
    
    for i in range(len(Edgeall)):
        srcTar = Edgeall[i]
        src = long(srcTar[0])
        tar = long(srcTar[1])

        # 使用滑动窗口缓冲边集
        win.append((src, tar))
        winedges = winedges + 1
        if winedges < window and i < len(Edgeall)-1:
            continue

        print len(win), winedges
        # exit(0)
        
        # 全局洗牌法初始化
        order = []
        for i in range(0, winedges):
            order.append(i)
        # 使用洗牌法得到加载序列
        for i in range(0, winedges):
            ttemp = random.randint(0, winedges - 1)
            temp = order[i]
            order[i] = order[ttemp]
            order[ttemp] = temp

        for i in range(0, winedges):
            srcTar = win[order[i]]
            src = long(srcTar[0])
            tar = long(srcTar[1])

            # print src, tar
            edgeNum = edgeNum + 1
            if edgeNum % 1000000 == 0:
                print edgeNum

            # 寻找当前子图的最大值和最小值
            maxsize = 0
            minsize = 100000000
            for i in range(numOfParts):
                if maxsize < len(Partitions[i]):
                    maxsize = len(Partitions[i])
                if minsize > len(Partitions[i]):
                    minsize = len(Partitions[i])
            print maxsize - minsize
            
            # 构建初始子图集合
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

            # 分边策略
            # print src
            # print tar
            # print srcMachines
            # print tarMachines
            # flag = flag + 1
            # if flag > 30:
            #     exit()

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
            # print partSocre2edge[part]

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

            # ver2degreeDic[src] = ver2degreeDic[src] + 1
            # ver2degreeDic[tar] = ver2degreeDic[tar] + 1

        win = []
        winedges = 0

        # if edgeNum == 1200:
        #     break
    
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

singleWindowGreedy("/home/w/data/Wiki-Vote.txt", 100)

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

