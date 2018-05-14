#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: PowerGraphPartitioning.py [edges_dataset] [numOfPartitions]

Notice: this program is used to partition a graph with proper size,
whose vertices table can be kept in memory, in PowerGraph way.
Thus, we need a distributed version to handle that too large graph.
'''


import sys
import random
from os import listdir
from os.path import isfile, join
#from sets import Set


def PowerGraphPar(edgesFile, numOfPar):

    # the file to be partitioned(edges file)
    partitionedFile = edgesFile
    # the number of partitions requested
    numOfPartitions = numOfPar

    # build a table to store the current number of edges in each partition
    parInfoTable = {}
    for i in range(1, numOfPartitions+1):
        parInfoTable[i] = 0

    # the number of edges(number of lines in partitionedFile)
    numEdges = 0

    # the number of vertices
    numOfVertices = 0

    # a dict to store the vertices in each partition
    vdic = {}
    # the partitioning results to display
    parRs = ""

    # build a table to store number of edges from each vertex and its machines assigned later, e.g. A(v)
    # {vertexId:(edgesNum, (machines))}
    verticesDict = {}
    with open(partitionedFile, 'r') as f:
        for line in f:
            # if line.startswith("#"):
            #    break

            numEdges = numEdges + 1
            srcTar = line.strip().split()
            # a -> b  => a follows b ??
            srcV = long(srcTar[0])
            # src = long(srcTar[1])
            tarV = long(srcTar[1])
            if srcV in verticesDict:
                verticesDict[srcV] = (verticesDict[srcV][0] + 1, set())
            else:
                # emptySet = set()
                verticesDict[srcV] = (1, set())

            if tarV not in verticesDict:
                verticesDict[tarV] = (0, set())

    # the max number of edges in each partition(file) obtained from partitioning
    edgesInEachFile = numEdges / numOfPartitions + numEdges % numOfPartitions

    # the files of partitions
    # sub_files = [open(partitionedFile + 'Sub_%i.txt' % i, 'w') for i in range(0, numOfPartitions)]

    # a list to store the edges and their partition id
    # [(1, 10, {"partition": 2}), ...]
    partitions = []

    count = 0
    with open(partitionedFile, 'r') as input:
        for line in input:
            # if line.startswith("#"):
            #    break

            count = count + 1
            print count

            srcTar = line.strip().split()
            # a -> b  => a follows b ??
            srcV = long(srcTar[0])
            # src = long(srcTar[1])
            tarV = long(srcTar[1])

            srcUnassigned = verticesDict[srcV][0]
            srcMachines = verticesDict[srcV][1]

            tarUnassigned = verticesDict[tarV][0]
            tarMachines = verticesDict[tarV][1]

            parId = -1

            #dic1 = {}
            #dic1["partition"] = parId
            #partitions.append((src, tar, dic1))

            if (not srcMachines) and (not tarMachines):
                # choose the 1st partition with min edges
                parId = min(parInfoTable, key=parInfoTable.get)
                dic1 = {}
                dic1["partition"] = parId
                partitions.append((srcV, tarV, dic1))
                parInfoTable[parId] = parInfoTable[parId] + 1
                # print srcMachines
                # print srcV
                srcMachines.add(parId)
                tarMachines.add(parId)
            else:
                if len(srcMachines) != 0 and len(tarMachines) != 0:
                    intersection = srcMachines & tarMachines
                    if (len(intersection) == 0):
                        tmp = set()
                        tmp2 = set()
                        if srcUnassigned > tarUnassigned:
                            tmp = srcMachines
                            tmp2 = tarMachines
                        else:
                            tmp = tarMachines
                            tmp2 = srcMachines
                        for t in tmp:
                            if parInfoTable[t] < edgesInEachFile:
                                parId = t
                                break
                        if parId == -1:
                            for t in tmp2:
                                if parInfoTable[t] < edgesInEachFile:
                                    parId = t
                                    break

                        if parId == -1:
                            parId = min(parInfoTable, key=parInfoTable.get)

                        #sub_files[parId].write(line)
                        dic1 = {}
                        dic1["partition"] = parId
                        partitions.append((srcV, tarV, dic1))

                        parInfoTable[parId] = parInfoTable[parId] + 1
                        srcMachines.add(parId)
                        tarMachines.add(parId)



                    else:
                        for t in intersection:
                            if parInfoTable[t] < edgesInEachFile:
                                parId = t
                                break
                        if parId == -1:
                            for t in (srcMachines | tarMachines) - intersection:
                                if parInfoTable[t] < edgesInEachFile:
                                    parId = t
                                    break
                        if parId == -1:
                            parId = min(parInfoTable, key=parInfoTable.get)

                        #sub_files[parId].write(line)
                        dic1 = {}
                        dic1["partition"] = parId
                        partitions.append((srcV, tarV, dic1))
                        parInfoTable[parId] = parInfoTable[parId] + 1
                        srcMachines.add(parId)
                        tarMachines.add(parId)

                else:
                    if (len(srcMachines) == 0 or len(tarMachines) == 0) and (len(srcMachines) + len(tarMachines)) > 0:
                        tmp = set()
                        if len(srcMachines) == 0:
                            tmp = tarMachines
                        else:
                            tmp = srcMachines

                        for t in tmp:
                            if parInfoTable[t] < edgesInEachFile:
                                parId = t
                                break

                        if parId == -1:
                            parId = min(parInfoTable, key=parInfoTable.get)

                        #sub_files[parId].write(line)
                        dic1 = {}
                        dic1["partition"] = parId
                        partitions.append((srcV, tarV, dic1))

                        parInfoTable[parId] = parInfoTable[parId] + 1
                        srcMachines.add(parId)
                        tarMachines.add(parId)

            verticesDict[srcV] = (verticesDict[srcV][0] - 1, verticesDict[srcV][1])

            if vdic.has_key(parId):
                vdic[parId].add(srcV)
                vdic[parId].add(tarV)
            else:
                vs = set()
                vs.add(srcV)
                vs.add(tarV)
                vdic[parId] = vs

    overall = 0L
    for id, vs in vdic.iteritems():
        overall += len(vs)
    vs = vdic[1]
    for i in range(2, int(numOfPar) + 1):
        vs.update(vdic[i])
    numOfVertices = len(vs)

    vrf = overall / float(numOfVertices)

    # to store/print the size of each partition
    sizeStr = ""
    for id, en in parInfoTable.iteritems():
        sizeStr += str(en) + "\n"

    # the partitioning result(string)
    parRs = "*PowerGraph Partitioning*\n" + "Vertices: " + str(numOfVertices) + "\n" + "Edges: " + str(numEdges) + "\n" + \
            "Size of Each Partition: \n" + sizeStr + "Vertex Replica Factor: \n" + str(vrf)

    return partitions, [], parRs

# ***************************************************


'''


# the file to be partitioned(edges file)
partitionedFile = sys.argv[1]
# the number of partitions requested
numOfPartitions = int(sys.argv[2])

# build a table to store the current number of edges in each partition
parInfoTable = {}
for i in range(0,numOfPartitions):
    parInfoTable[i] = 0
    
    

# the number of edges(number of lines in partitionedFile)
numEdges = 0

# build a table to store number of edges from each vertex and its machines assigned later, e.g. A(v)
# {vertexId:(edgesNum, (machines))}
verticesDict = {}
with open(partitionedFile, 'r') as f:
    for line in f:
        #if line.startswith("#"):
        #    break
        
        numEdges = numEdges + 1
        srcV, tarV = line.strip().split()
        if srcV in verticesDict:
            verticesDict[srcV] = (verticesDict[srcV][0]+1, set())
        else:
            #emptySet = set()
            verticesDict[srcV] = (1, set())
            
        if tarV not in verticesDict:
            verticesDict[tarV] = (0, set())
        
print 'the number of edges: '+str(numEdges)
print verticesDict['1']

# the max number of edges in each partition(file) obtained from partitioning
edgesInEachFile = numEdges/numOfPartitions + numEdges%numOfPartitions

# the files of partitions
sub_files = [open(partitionedFile+'Sub_%i.txt' %i, 'w') for i in range(0,numOfPartitions)]

count = 0
with open(partitionedFile, 'r') as input:
    for line in input:
        #if line.startswith("#"):
        #    break
        
        count = count + 1
        print count
        
        srcV, tarV = line.strip().split()
        
        srcUnassigned = verticesDict[srcV][0]
        srcMachines = verticesDict[srcV][1]
        
        tarUnassigned = verticesDict[tarV][0]
        tarMachines = verticesDict[tarV][1]
        
        parId = -1
        
        if (not srcMachines) and (not tarMachines):
            # choose the 1st partition with min edges
            parId = min(parInfoTable, key=parInfoTable.get)
            sub_files[parId].write(line)
            parInfoTable[parId] = parInfoTable[parId]+1
            #print srcMachines
            #print srcV
            srcMachines.add(parId)
            tarMachines.add(parId)
        else:    
            if len(srcMachines)!=0 and len(tarMachines)!=0:
                intersection = srcMachines & tarMachines
                if(len(intersection)==0):
                    tmp = set()
                    tmp2 = set()
                    if srcUnassigned > tarUnassigned:
                        tmp = srcMachines
                        tmp2 = tarMachines
                    else:
                        tmp = tarMachines
                        tmp2 = srcMachines
                    for t in tmp:
                        if parInfoTable[t] < edgesInEachFile:
                            parId = t
                            break
                    if parId == -1:
                        for t in tmp2:
                            if parInfoTable[t] < edgesInEachFile:
                                parId = t
                                break
                                    
                    if parId == -1:
                        parId = min(parInfoTable, key=parInfoTable.get)
                    
                    sub_files[parId].write(line)
                    parInfoTable[parId] = parInfoTable[parId]+1
                    srcMachines.add(parId)
                    tarMachines.add(parId)
                    
                    
                    
                else:
                    for t in intersection:
                        if parInfoTable[t] < edgesInEachFile:
                            parId = t
                            break
                    if parId == -1:
                        for t in (srcMachines|tarMachines)-intersection:
                            if parInfoTable[t] < edgesInEachFile:
                                parId = t
                                break
                    if parId == -1:
                        parId = min(parInfoTable, key=parInfoTable.get)
                        
                    sub_files[parId].write(line)
                    parInfoTable[parId] = parInfoTable[parId]+1
                    srcMachines.add(parId)
                    tarMachines.add(parId)
                
            else:
                if (len(srcMachines)==0 or len(tarMachines)==0) and (len(srcMachines)+len(tarMachines))>0:
                    tmp = set()
                    if len(srcMachines)==0:
                        tmp = tarMachines
                    else:
                        tmp = srcMachines
                        
                    for t in tmp:
                        if parInfoTable[t] < edgesInEachFile:
                            parId = t
                            break
                            
                    if parId == -1:
                        parId = min(parInfoTable, key=parInfoTable.get)
                        
                    sub_files[parId].write(line)
                    parInfoTable[parId] = parInfoTable[parId]+1
                    srcMachines.add(parId)
                    tarMachines.add(parId)
        
        verticesDict[srcV] = (verticesDict[srcV][0]-1, verticesDict[srcV][1])
        


for f in sub_files:
    f.close()

'''
    
        

