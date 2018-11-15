#!/usr/bin/python
# -*- coding: utf-8 -*-

# 完整的swr方案实现

import random
import math
import time

time_start = time.time()

# 划分子图数量
numOfParts = 100
# 窗口大小上升速率
q = 2
# 窗口大小下降速率
p = 0
# 存储总边数
edgeNum = 0
# 窗口初始大小
windowsize = 100000
# 最大窗口大小
maxwindowsize = 10000000000
# 窗口上升调整阈值
thresholdup = 0.000001
# 窗口下降调整阈值
thresholddown = 0.00000001
# 考虑neighbors的情况的阈值,在最小的多少个子图中选择邻居节点最多的分区
thresholdneighbors = 1
# 每次分配边的比例
AssignProportion = 0.1

# [[(src, dst), (src, dst),...],[()],[()]....]          每个分区对应的边集合
Partitions = [[] for i in range(numOfParts)]
# { part:set(v1,v2,...), ... }                          存储每个分区对应的点
vertexDic = {}
# { vertex:set(part1, part2,...),... }                  存储每个点对应的分区
ver2partDic = {}
# { vertex:degree,... }                                 存储每个点对应的度信息
ver2degreeDic = {}
# { (part, vertex):times, ...}                          存储每个点在每个Partition中出现的次数
partVertexTimes = {}

edges = []
window = []
f = open("/home/w/data/testdata/bfs1.txt", "r")
for line in f:
    srcTar = line.strip().split()
    src = long(srcTar[0])
    tar = long(srcTar[1])
    edges.append((src, tar))

for i in range(numOfParts):
    vertexDic[i] = set()

line = 0  # 记录当前处理的是第几条边
while(line < len(edges)):
    while(len(window) < windowsize and line < len(edges)):   # 将窗口填满，或者是最后一点了
        window.append(edges[line])
        line = line + 1
    if(len(window) < windowsize):                            # 最后一点时，修正windowsize
        windowsize = len(window)
    print windowsize
    random.shuffle(window)
    if(line == len(edges)):
        AssignProportion = 1
    removeLen = int(len(window) * AssignProportion)
    # 进行本轮的分配
    for i in range(removeLen):
        src = window[i][0]
        tar = window[i][1]
        
        # 更新src和tar所存在的Partition和全局的度信息
        edgeNum = edgeNum + 1
        if(ver2partDic.has_key(src)):
            srcMachines = ver2partDic[src]
        else:
            ver2partDic[src] = set()
            srcMachines = ver2partDic[src]
        if(ver2partDic.has_key(tar)):
            tarMachines = ver2partDic[tar]
        else:
            ver2partDic[tar] = set()
            tarMachines = ver2partDic[tar]
        if(ver2degreeDic.has_key(src)):
            srcDegree = ver2degreeDic[src]
        else:
            ver2degreeDic[src] = 0
            srcDegree = 0
        if(ver2degreeDic.has_key(tar)):
            tarDegree = ver2degreeDic[tar]
        else:
            ver2degreeDic[tar] = 0
            tarDegree = 0

        # 开始根据策略对边进行分配
        part = -1
        # src和tar都没有出现的情况
        if((len(srcMachines)==0)and(len(tarMachines)==0)):
            for j in range(numOfParts):
                if(part==-1):
                    part = j
                    continue
                if(len(Partitions[j])<len(Partitions[part])):
                    part = j

        # src出现但是tar不出现的情况
        elif((len(srcMachines)>0)and(len(tarMachines)==0)):
            srcList = []                                             # [(len(Partition), part), ...]
            for j in srcMachines:
                srcList.append((len(Partitions[j]), j))
            srcList.sort(key=lambda x:x[0], reverse=False)
            for j in range(min(thresholdneighbors, len(srcList))):
                if(part==-1):
                    part = srcList[0][1]
                    continue
                if(partVertexTimes[(srcList[j][1], src)] > partVertexTimes[(part, src)]):
                    part = srcList[j][1]

        # src不出现但是tar出现的情况
        elif((len(srcMachines)==0)and(len(tarMachines)>0)):
            tarList = []                                             # [(len(Partition), part), ...]
            for j in tarMachines:
                tarList.append((len(Partitions[j]), j))
            tarList.sort(key=lambda x:x[0], reverse=False)
            for j in range(min(thresholdneighbors, len(tarList))):
                if(part==-1):
                    part = tarList[0][1]
                    continue
                if(partVertexTimes[(tarList[j][1], tar)] > partVertexTimes[(part, tar)]):
                    part = tarList[j][1]

        # src和tar都出现的情况
        else:
            Intersection = srcMachines & tarMachines
            Convergence = srcMachines | tarMachines
            # src和tar有交集的情况
            if(len(Intersection) > 0):
                srcTarList = []                                      # [(len(Partition), part), ...]
                for j in Intersection:
                    srcTarList.append((len(Partitions[j]), j))
                srcTarList.sort(key=lambda x:x[0], reverse=False)
                part = srcTarList[0][1]
                for j in range(min(thresholdneighbors, len(srcTarList))):
                    if(part==-1):
                        part = srcTarList[0][1]
                        continue
                    if(partVertexTimes[(srcTarList[j][1], src)] + partVertexTimes[(srcTarList[j][1], tar)] > \
                        partVertexTimes[(part, src)] + partVertexTimes[(part, tar)]):
                        part = srcTarList[j][1]
            # src和tar没有交集的情况
            else:
                if(srcDegree > tarDegree):
                    tarList = []                                             # [(len(Partition), part), ...]
                    for j in tarMachines:
                        tarList.append((len(Partitions[j]), j))
                    tarList.sort(key=lambda x:x[0], reverse=False)
                    part = tarList[0][1]
                    for j in range(min(thresholdneighbors, len(tarList))):
                        if(part==-1):
                            part = tarList[0][1]
                            continue
                        if(partVertexTimes[(tarList[j][1], tar)] > partVertexTimes[(part, tar)]):
                            part = tarList[j][1]
                else:
                    srcList = []                                             # [(len(Partition), part), ...]
                    for j in srcMachines:
                        srcList.append((len(Partitions[j]), j))
                    srcList.sort(key=lambda x:x[0], reverse=False)
                    part = srcList[0][1]
                    for j in range(min(thresholdneighbors, len(srcList))):
                        if(part==-1):
                            part = srcList[0][1]
                            continue
                        if(partVertexTimes[(srcList[j][1], src)] > partVertexTimes[(part, src)]):                         
                            part = srcList[j][1]

        # 得到target part，更新相关数据
        Partitions[part].append((src, tar))
        vertexDic[part].add(src)
        vertexDic[part].add(tar)
        ver2partDic[src].add(part)
        ver2partDic[tar].add(part)
        ver2degreeDic[src] = ver2degreeDic[src] + 1
        ver2degreeDic[tar] = ver2degreeDic[tar] + 1
        if(partVertexTimes.has_key((part, src))):
            partVertexTimes[(part, src)] = partVertexTimes[(part, src)] + 1
        else:
            partVertexTimes[(part, src)] = 0
        if(partVertexTimes.has_key((part, tar))):
            partVertexTimes[(part, tar)] = partVertexTimes[(part, tar)] + 1
        else:
            partVertexTimes[(part, tar)] = 0
        
    # 修正窗口大小和内容
    window = window[removeLen:windowsize]
    maxPartition = 0
    minPartition = 1000000000
    for i in range(numOfParts):
        if(maxPartition < len(Partitions[i])):
            maxPartition = len(Partitions[i])
        if(minPartition > len(Partitions[i])):
            minPartition = len(Partitions[i])
    balance = float(maxPartition - minPartition)/float(maxPartition + minPartition)
    if(balance > thresholdup):
        windowsize = int(windowsize * (1.0+q))
    if(balance < thresholddown):
        windowsize = int(windowsize / (1.0+p))
    if(windowsize > maxwindowsize):
        windowsize = maxwindowsize

# 全部分配完成，统计数据
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

print edgeNum
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

time_end = time.time()
time_used = time_end - time_start
print "time " + str(time_used)
