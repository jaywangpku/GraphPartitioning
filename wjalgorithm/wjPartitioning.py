#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def wjAL(edgelist, numOfParts):
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # { vertex:set(part1, part2,...),... }          存储每个点对应的分区
    ver2partDic = {}
    # { vertex:degree,... }                         存储每个点对应的度信息
    ver2degreeDic = {}

    # 存储总边数
    edgeNum = 0

    # 构建高度数顶点集
    highDegVer = []                      # [(vertex:degree), (vertex:degree),,,,]  按照元组访问规则即可访问
    highDegVerNum = 800                  # 全局高度数点选择个数
    highDegVerNumOfBufs = 3              # buf中高度数点选择个数


    # 缓冲区大小控制
    bufs = 1000
    buf = 0
    edgeBuf = []
    vertexBuf = set()
    edgePartNum = 10

    # 每个子图对应的高度数点集   {part:set(hv1, hv2, ...) ...}
    HighVerDeg4Parts = {}
    for i in range(numOfParts):
        HighVerDeg4Parts[i] = set()

    # 状态标记变量
    edgefileOver = 0
    Iterative = 1
    
    # 调试变量
    flag = 0

    for i in range(numOfParts):
        vertexDic[i] = set()

    lines = f.readlines()
    for i_edge in range(len(lines)):
        line = lines[i_edge]
        if i_edge == len(lines) - 1:
            edgefileOver = 1
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        
        edgeNum = edgeNum + 1
        if edgeNum % 1000000 == 0:
            print edgeNum

        # 每一轮将缓冲区填满后进行后续划分操作 
        buf = len(edgeBuf)
        if buf < bufs:
            edgeBuf.append((src, tar))
            # 全部节点对应的度信息
            if ver2degreeDic.has_key(src):
                ver2degreeDic[src] = ver2degreeDic[src] + 1
            else:
                ver2degreeDic[src] = 1
            if ver2degreeDic.has_key(tar):
                ver2degreeDic[tar] = ver2degreeDic[tar] + 1
            else:
                ver2degreeDic[tar] = 1
            buf = buf + 1
            # 如果已经没有边了，则处理最后一批
            if edgefileOver == 1:
                break
            continue    

        # 如果不是最后阶段
        if edgefileOver == 0:
            print "第 %d 次迭代"%(Iterative)
            Iterative = Iterative + 1

            # if Iterative > 100:
            #     exit(0)
            # 构建缓冲区子图
            # g = nx.Graph()
            # for i in range(bufs):
            #     g.add_edge(edgeBuf[i][0], edgeBuf[i][1])
            # nx.draw(g, node_size = 20, node_color = 'r')
            # plt.show()

            # 需要找到度数最大的几个点
            afterSortALL = sorted(ver2degreeDic.items(), key=lambda e:e[1], reverse = True)
            if len(afterSortALL) > highDegVerNum:
                highDegVer = afterSortALL[0:highDegVerNum]
            else:
                highDegVer = afterSortALL[0: len(afterSortALL)]
            # print highDegVer


            # 获取当前bufs中度数最大的几个点
            # { vertex:degree,... }                         存储每个点对应的度信息
            BufsVer2degreeDic = {}

            # 获取目前 bufs 里面存在的高度数点的前两位
            for i in range(len(edgeBuf)):
                src = edgeBuf[i][0]
                tar = edgeBuf[i][1]

                if BufsVer2degreeDic.has_key(src):
                    BufsVer2degreeDic[src] = BufsVer2degreeDic[src] + 1
                else:
                    BufsVer2degreeDic[src] = 1
                if BufsVer2degreeDic.has_key(tar):
                    BufsVer2degreeDic[tar] = BufsVer2degreeDic[tar] + 1
                else:
                    BufsVer2degreeDic[tar] = 1

                vertexBuf.add(src)
                vertexBuf.add(tar)

            afterSortBufs = sorted(BufsVer2degreeDic.items(), key=lambda e:e[1], reverse = True)

            # 获取在set中存在的高度数点
            highDegVerSet = []
            for i in range(len(highDegVer)):
                if highDegVer[i][0] in vertexBuf:
                    highDegVerSet.append(highDegVer[i][0])
            # print highDegVerSet
            
            # 选择添加一定的局部高度数点
            for i in range(highDegVerNumOfBufs):
                if afterSortBufs[i][0] not in highDegVerSet:
                    highDegVerSet.append(afterSortBufs[i][0])

            # 存储当前bufs情况下，对应的高度数点点集信息
            # {highvertex:set(), ... }
            highDegVer2Set = {}
            for i in range(len(highDegVerSet)):
                highDegVer2Set[highDegVerSet[i]] = set()
            
            # 获取与每个高度数点都直接相连的点集
            for i in range(len(edgeBuf)):
                src = edgeBuf[i][0]
                tar = edgeBuf[i][1]
                if src in highDegVerSet:
                    highDegVer2Set[src].add(tar)
                if tar in highDegVerSet:
                    highDegVer2Set[tar].add(src)

            # for (k,v) in highDegVer2Set.items():
            #     print k, v

            # 存储双点映射结构    {(v1,v2):set(v3,v4,v5, ...), ...}
            doubleMapedge = {}
            highV1 = highDegVerSet[0]
            highV2 = highDegVerSet[1]
            for i in range(len(highDegVerSet)):
                for j in range(i + 1, len(highDegVerSet)):
                    doubleMapedge[(highDegVerSet[i], highDegVerSet[j])] = highDegVer2Set[highDegVerSet[i]] & highDegVer2Set[highDegVerSet[j]]
                    if len(doubleMapedge[(highDegVerSet[i], highDegVerSet[j])]) > len(doubleMapedge[(highV1, highV2)]):
                        highV1 = highDegVerSet[i]
                        highV2 = highDegVerSet[j]

            #         print (highDegVerSet[i], highDegVerSet[j])
            #         print doubleMapedge[(highDegVerSet[i], highDegVerSet[j])]
            # print highV1, highV2

            # 找到双点映射信息对应的全部的边
            edgePart = []
            for i in range(len(edgeBuf)):
                src = edgeBuf[i][0]
                tar = edgeBuf[i][1]
                if src == highV1 and tar == highV2:
                    edgePart.append((src, tar))
                elif src == highV2 and tar == highV1:
                    edgePart.append((src, tar))
                elif (src == highV1 and (tar in doubleMapedge[(highV1, highV2)])):
                    edgePart.append((src, tar))
                elif (src == highV2 and (tar in doubleMapedge[(highV1, highV2)])):
                    edgePart.append((src, tar))
                elif (tar == highV1 and (src in doubleMapedge[(highV1, highV2)])):
                    edgePart.append((src, tar))
                elif (tar == highV2 and (src in doubleMapedge[(highV1, highV2)])):
                    edgePart.append((src, tar))

            
            if len(edgePart) < edgePartNum:
                edgePart = []
                print "单点度数最大策略"
            else:
                print "双点映射策略"
                print "len(edgePart)", len(edgePart)

            # 如果不存在这样的指定结构的边,将最高度数点对应的边加入到一个指定分区
            highV = -1
            if len(edgePart) == 0:
                highV = afterSortBufs[0][0]
                for i in range(len(edgeBuf)):
                    src = edgeBuf[i][0]
                    tar = edgeBuf[i][1]
                    if src == highV or tar == highV:
                        edgePart.append((src, tar))
            
            print "len(edgePart)", len(edgePart)

            # 删除 bufs 缓冲区中的边
            for i in range(len(edgePart)):
                edgeBuf.remove(edgePart[i])

            print len(edgeBuf)

            # print edgePart
            
            # 将找到的边进行分配
            # 先找出一份可选Part集
            TempPartsTwo = []                          # 两个点都存在该Partition中
            TempPartsOne = []                          # 只有一个点存在该Partition中
            TempPartsNone = []                         # 有元素，但没有一个Partition存在这两个点
            TempPartsNothing = []                      # 该part没有任何元素

            TempPart4One = []                          # 只有一个highV的情况
            
            if highV == -1:
                for i in range(numOfParts):
                    if highV1 in HighVerDeg4Parts[i] and highV2 in HighVerDeg4Parts[i]:
                        TempPartsTwo.append(i)
                    elif highV1 in HighVerDeg4Parts[i] and highV2 not in HighVerDeg4Parts[i]:
                        TempPartsOne.append(i)
                    elif highV1 not in HighVerDeg4Parts[i] and highV2 in HighVerDeg4Parts[i]:
                        TempPartsOne.append(i)
                    else :
                        if len(Partitions[i]) > 0:
                            TempPartsNone.append(i)
                        else:
                            TempPartsNothing.append(i)
            else :
                for i in range(numOfParts):
                    if highV in HighVerDeg4Parts[i]:
                        TempPart4One.append(i)

            part = 0
            if highV == -1:
                # 首先如果存在两个点都在一个子图中，则优先放入该子图
                if len(TempPartsTwo) > 0:
                    minPart = TempPartsTwo[0]
                    for i in range(len(TempPartsTwo)):
                        if len(Partitions[minPart]) > len(Partitions[TempPartsTwo[i]]):
                            minPart = TempPartsTwo[i]
                    part = minPart
                # 如果不存在这样相同的两个高度数点在同一子图中，则优先放入空part中
                elif len(TempPartsTwo) == 0 and len(TempPartsNothing) > 0:
                    part = TempPartsNothing[0]
                    HighVerDeg4Parts[part].add(highV1)
                    HighVerDeg4Parts[part].add(highV2)
                # 如果只存在一个点在高度数顶点中，且没有空part，则选择放入一个高度数顶点对应的子图中
                elif len(TempPartsTwo) == 0 and len(TempPartsNothing) == 0 and len(TempPartsOne) > 0:
                    minPart = TempPartsOne[0]
                    for i in range(len(TempPartsOne)):
                        if len(Partitions[minPart]) > len(Partitions[TempPartsOne[i]]):
                            minPart = TempPartsOne[i]
                    part = minPart
                    HighVerDeg4Parts[part].add(highV1)
                    HighVerDeg4Parts[part].add(highV2)
                # 如果不存在子图有这两个高度数点，且没有空part
                elif len(TempPartsTwo) == 0 and len(TempPartsNothing) == 0 and len(TempPartsOne) == 0 and len(TempPartsNone) > 0:
                    minPart = TempPartsNone[0]
                    for i in range(len(TempPartsNone)):
                        if len(Partitions[minPart]) > len(Partitions[TempPartsNone[i]]):
                            minPart = TempPartsNone[i]
                    part = minPart
                    HighVerDeg4Parts[part].add(highV1)
                    HighVerDeg4Parts[part].add(highV2)
            # 只有一个highV的情况，选择满足条件且边数最少的子图
            else:
                if len(TempPart4One) > 0:
                    minPart = TempPart4One[0]
                    for i in range(len(TempPart4One)):
                        if len(Partitions[minPart]) > len(Partitions[TempPart4One[i]]):
                            minPart = TempPart4One[i]
                    part = minPart
                else:
                    minPart = 0
                    for i in range(numOfParts):
                        if len(Partitions[minPart]) > len(Partitions[i]):
                            minPart = i
                    part = minPart
                HighVerDeg4Parts[part].add(highV)


            # 根据part，将需要分配的边进行分配
            for i in range(len(edgePart)):
                Partitions[part].append(edgePart[i])
                vertexDic[part].add(edgePart[i][0])
                vertexDic[part].add(edgePart[i][1])

            # print Partitions[0]
            # print '\n'
            # print Partitions[1]
            # print "\n\n\n"


        # 如果是最后一个阶段
        elif edgefileOver == 1:
            print "进入最后一个阶段"

            # 构建缓冲区子图
            # g = nx.Graph()
            # for i in range(bufs):
            #     g.add_edge(edgeBuf[i][0], edgeBuf[i][1])
            # nx.draw(g, node_size = 20, node_color = 'r')
            # plt.show()

            # 需要找到度数最大的几个点
            afterSortALL = sorted(ver2degreeDic.items(), key=lambda e:e[1], reverse = True)
            highDegVer = afterSortALL[0:highDegVerNum]
            # print highDegVer


            # 获取当前bufs中度数最大的几个点
            # { vertex:degree,... }                         存储每个点对应的度信息
            BufsVer2degreeDic = {}

            # 获取目前 bufs 里面存在的高度数点的前两位
            for i in range(len(edgeBuf)):
                src = edgeBuf[i][0]
                tar = edgeBuf[i][1]

                if BufsVer2degreeDic.has_key(src):
                    BufsVer2degreeDic[src] = BufsVer2degreeDic[src] + 1
                else:
                    BufsVer2degreeDic[src] = 1
                if BufsVer2degreeDic.has_key(tar):
                    BufsVer2degreeDic[tar] = BufsVer2degreeDic[tar] + 1
                else:
                    BufsVer2degreeDic[tar] = 1

                vertexBuf.add(src)
                vertexBuf.add(tar)

            afterSortBufs = sorted(BufsVer2degreeDic.items(), key=lambda e:e[1], reverse = True)

            # 获取在set中存在的高度数点
            highDegVerSet = []
            for i in range(highDegVerNum):
                if highDegVer[i][0] in vertexBuf:
                    highDegVerSet.append(highDegVer[i][0])
            # print highDegVerSet
            
            # 选择添加一定的局部高度数点
            for i in range(highDegVerNumOfBufs):
                if afterSortBufs[i][0] not in highDegVerSet:
                    highDegVerSet.append(afterSortBufs[i][0])

            # 存储当前bufs情况下，对应的高度数点点集信息
            # {highvertex:set(), ... }
            highDegVer2Set = {}
            for i in range(len(highDegVerSet)):
                highDegVer2Set[highDegVerSet[i]] = set()
            
            # 获取与每个高度数点都直接相连的点集
            for i in range(len(edgeBuf)):
                src = edgeBuf[i][0]
                tar = edgeBuf[i][1]
                if src in highDegVerSet:
                    highDegVer2Set[src].add(tar)
                if tar in highDegVerSet:
                    highDegVer2Set[tar].add(src)

            # for (k,v) in highDegVer2Set.items():
            #     print k, v

            # 存储双点映射结构    {(v1,v2):set(v3,v4,v5, ...), ...}
            # 将双点映射结构全部的边都按照一定的规则分入子图
            doubleMapedge = {}
            edgePart = []
            for i in range(len(highDegVerSet)):
                for j in range(i + 1, len(highDegVerSet)):
                    doubleMapedge[(highDegVerSet[i], highDegVerSet[j])] = highDegVer2Set[highDegVerSet[i]] & highDegVer2Set[highDegVerSet[j]]
                    highV1 = highDegVerSet[i]
                    highV2 = highDegVerSet[j]
                    for i in range(len(edgeBuf)):
                        src = edgeBuf[i][0]
                        tar = edgeBuf[i][1]
                        if src == highV1 and tar == highV2:
                            edgePart.append((src, tar))
                        elif src == highV2 and tar == highV1:
                            edgePart.append((src, tar))
                        elif (src == highV1 and (tar in doubleMapedge[(highV1, highV2)])):
                            edgePart.append((src, tar))
                        elif (src == highV2 and (tar in doubleMapedge[(highV1, highV2)])):
                            edgePart.append((src, tar))
                        elif (tar == highV1 and (src in doubleMapedge[(highV1, highV2)])):
                            edgePart.append((src, tar))
                        elif (tar == highV2 and (src in doubleMapedge[(highV1, highV2)])):
                            edgePart.append((src, tar))
                    
                    if len(edgePart) > 0:
                        TempPartsTwo = []                          # 两个点都存在该Partition中
                        TempPartsOne = []                          # 只有一个点存在该Partition中
                        TempPartsNone = []                         # 有元素，但没有一个Partition存在这两个点
                        TempPartsNothing = []                      # 该part没有任何元素
                        for i in range(numOfParts):
                            if highV1 in HighVerDeg4Parts[i] and highV2 in HighVerDeg4Parts[i]:
                                TempPartsTwo.append(i)
                            elif highV1 in HighVerDeg4Parts[i] and highV2 not in HighVerDeg4Parts[i]:
                                TempPartsOne.append(i)
                            elif highV1 not in HighVerDeg4Parts[i] and highV2 in HighVerDeg4Parts[i]:
                                TempPartsOne.append(i)
                            else :
                                if len(Partitions[i]) > 0:
                                    TempPartsNone.append(i)
                                else:
                                    TempPartsNothing.append(i)
                        
                        part = -1
                        # 首先如果存在两个点都在一个子图中，则优先放入该子图
                        if len(TempPartsTwo) > 0:
                            minPart = TempPartsTwo[0]
                            for i in range(len(TempPartsTwo)):
                                if len(Partitions[minPart]) > len(Partitions[TempPartsTwo[i]]):
                                    minPart = TempPartsTwo[i]
                            part = minPart
                        # 如果不存在这样相同的两个高度数点在同一子图中，则优先放入空part中
                        elif len(TempPartsTwo) == 0 and len(TempPartsNothing) > 0:
                            part = TempPartsNothing[0]
                            HighVerDeg4Parts[part].add(highV1)
                            HighVerDeg4Parts[part].add(highV2)
                        # 如果只存在一个点在高度数顶点中，且没有空part，则选择放入一个高度数顶点对应的子图中
                        elif len(TempPartsTwo) == 0 and len(TempPartsNothing) == 0 and len(TempPartsOne) > 0:
                            minPart = TempPartsOne[0]
                            for i in range(len(TempPartsOne)):
                                if len(Partitions[minPart]) > len(Partitions[TempPartsOne[i]]):
                                    minPart = TempPartsOne[i]
                            part = minPart
                            HighVerDeg4Parts[part].add(highV1)
                            HighVerDeg4Parts[part].add(highV2)
                        # 如果不存在子图有这两个高度数点，且没有空part
                        elif len(TempPartsTwo) == 0 and len(TempPartsNothing) == 0 and len(TempPartsOne) == 0 and len(TempPartsNone) > 0:
                            minPart = TempPartsNone[0]
                            for i in range(len(TempPartsNone)):
                                if len(Partitions[minPart]) > len(Partitions[TempPartsNone[i]]):
                                    minPart = TempPartsNone[i]
                            part = minPart
                            HighVerDeg4Parts[part].add(highV1)
                            HighVerDeg4Parts[part].add(highV2)

                        for i in range(len(edgePart)):
                            Partitions[part].append(edgePart[i])
                            vertexDic[part].add(edgePart[i][0])
                            vertexDic[part].add(edgePart[i][1])
                        for i in range(len(edgePart)):
                            edgeBuf.remove(edgePart[i])

            # 其他的边按照顶点度数信息进行分配
            while len(edgeBuf) > 0:

                # 获取当前bufs中度数最大的几个点
                # { vertex:degree,... }                         存储每个点对应的度信息
                BufsVer2degreeDic = {}

                # 获取目前 bufs 里面存在的高度数点的前两位
                for i in range(len(edgeBuf)):
                    src = edgeBuf[i][0]
                    tar = edgeBuf[i][1]

                    if BufsVer2degreeDic.has_key(src):
                        BufsVer2degreeDic[src] = BufsVer2degreeDic[src] + 1
                    else:
                        BufsVer2degreeDic[src] = 1
                    if BufsVer2degreeDic.has_key(tar):
                        BufsVer2degreeDic[tar] = BufsVer2degreeDic[tar] + 1
                    else:
                        BufsVer2degreeDic[tar] = 1

                    vertexBuf.add(src)
                    vertexBuf.add(tar)

                afterSortBufs = sorted(BufsVer2degreeDic.items(), key=lambda e:e[1], reverse = True)
                
                highV = afterSortBufs[0][0]
                edgePart = []
                TempPart4One = []
                for i in range(len(edgeBuf)):
                    src = edgeBuf[i][0]
                    tar = edgeBuf[i][1]
                    if src == highV or tar == highV:
                        edgePart.append((src, tar))
                for i in range(numOfParts):
                    if highV in HighVerDeg4Parts[i]:
                        TempPart4One.append(i)

                part = 0
                minPart = TempPart4One[0]
                for i in range(len(TempPart4One)):
                    if len(Partitions[minPart]) > len(Partitions[TempPart4One[i]]):
                        minPart = TempPart4One[i]
                part = minPart
                HighVerDeg4Parts[part].add(highV)

                for i in range(len(edgePart)):
                    Partitions[part].append(edgePart[i])
                    vertexDic[part].add(edgePart[i][0])
                    vertexDic[part].add(edgePart[i][1])

                for i in range(len(edgePart)):
                    edgeBuf.remove(edgePart[i])

     
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

# wjAL("/home/w/data/Wiki-VoteRandom.txt", 20)
wjAL("/home/w/data/Wiki-Vote.txt", 20)

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

