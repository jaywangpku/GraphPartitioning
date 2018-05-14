#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
the random-based edge partitioning methods, from GraphX

"""
import random
import math

# Random Vertex Cut
def RVC(edgesFile, numOfPar):
    f = open(edgesFile, "r")
    # a list to store the edges and their partition id
    # [(1, 10, {"partition": 2}), ...]
    partitions = []
    # the number of edges
    numOfEdges = 0
    # the number of vertices
    numOfVertices = 0

    # a dict to store the vertices in each partition
    vdic = {}
    # a dict to store the number of edges in each partition
    ndic = {}
    parRs = ""
    for line in f:
        numOfEdges += 1
        srcTar = line.strip().split()
        # a -> b  => a follows b ??
        src = long(srcTar[0])
        # src = long(srcTar[1])
        tar = long(srcTar[1])

        parId = random.randint(1, int(numOfPar))
        dic1 = {}
        dic1["partition"] = parId
        partitions.append((src, tar, dic1))

        if ndic.has_key(parId):
            num = ndic[parId]
            ndic[parId] = num+1
        else:
            ndic[parId] = 1L

        if vdic.has_key(parId):
            vdic[parId].add(src)
            vdic[parId].add(tar)
        else:
            vs = set()
            vs.add(src)
            vs.add(tar)
            vdic[parId] = vs

    overall = 0L
    for id, vs in vdic.iteritems():
        overall += len(vs)
    vs = vdic[1]
    for i in range(2, int(numOfPar)+1):
        vs.update(vdic[i])
    numOfVertices = len(vs)

    vrf = overall/float(numOfVertices)

    # to store/print the size of each partition
    sizeStr = ""
    for id, en in ndic.iteritems():
        sizeStr += str(en) + "\n"

    # the partitioning result(string)
    parRs = "*RVC Partitioning*\n" + "Vertices: " + str(numOfVertices) + "\n" + "Edges: " + str(numOfEdges) + "\n" + \
             "Size of Each Partition: \n" + sizeStr + "Vertex Replica Factor: \n" + str(vrf)


    return partitions, [], parRs

# Canonical Random Vertex Cut
def CRV(edgesFile, numOfPar):
    f = open(edgesFile, "r")
    # a list to store the edges and their partition id
    # [(1, 10, {"partition": 2}), ...]
    partitions = []
    # the number of edges
    numOfEdges = 0
    # the number of vertices
    numOfVertices = 0

    # a dict to store the vertices in each partition
    vdic = {}
    # a dict to store the number of edges in each partition
    ndic = {}
    parRs = ""
    for line in f:
        numOfEdges += 1
        srcTar = line.strip().split()
        # a -> b  => a follows b ??
        src = long(srcTar[0])
        # src = long(srcTar[1])
        tar = long(srcTar[1])

        #parId = random.randint(1, int(numOfPar))
        mixingPrime = 1125899906842597L
        if(src < tar):
            parId = abs(hash((src*mixingPrime, tar))) % numOfPar
        else:
            parId = abs(hash((tar*mixingPrime, src))) % numOfPar
        dic1 = {}
        dic1["partition"] = parId
        partitions.append((src, tar, dic1))

        if ndic.has_key(parId):
            num = ndic[parId]
            ndic[parId] = num+1
        else:
            ndic[parId] = 1L

        if vdic.has_key(parId):
            vdic[parId].add(src)
            vdic[parId].add(tar)
        else:
            vs = set()
            vs.add(src)
            vs.add(tar)
            vdic[parId] = vs

    overall = 0L
    for id, vs in vdic.iteritems():
        overall += len(vs)
    vs = set()
    for key, vertices in vdic.iteritems():
        vs.update(vertices)
    numOfVertices = len(vs)

    vrf = overall/float(numOfVertices)

    # to store/print the size of each partition
    sizeStr = ""
    for id, en in ndic.iteritems():
        sizeStr += str(en) + "\n"

    # the partitioning result(string)
    parRs = "*CRV Partitioning*\n" + "Vertices: " + str(numOfVertices) + "\n" + "Edges: " + str(numOfEdges) + "\n" + \
             "Size of Each Partition: \n" + sizeStr + "Vertex Replica Factor: \n" + str(vrf)


    return partitions, [], parRs

# EdgePartition1D
def EP1D(edgesFile, numOfPar):
    f = open(edgesFile, "r")
    # a list to store the edges and their partition id
    # [(1, 10, {"partition": 2}), ...]
    partitions = []
    # the number of edges
    numOfEdges = 0
    # the number of vertices
    numOfVertices = 0

    # a dict to store the vertices in each partition
    vdic = {}
    # a dict to store the number of edges in each partition
    ndic = {}
    parRs = ""
    for line in f:
        numOfEdges += 1
        srcTar = line.strip().split()
        # a -> b  => a follows b ??
        src = long(srcTar[0])
        # src = long(srcTar[1])
        tar = long(srcTar[1])

        mixingPrime = 1125899906842597L
        parId = int(abs(src * mixingPrime) % numOfPar)

        dic1 = {}
        dic1["partition"] = parId
        partitions.append((src, tar, dic1))

        if ndic.has_key(parId):
            num = ndic[parId]
            ndic[parId] = num+1
        else:
            ndic[parId] = 1L

        if vdic.has_key(parId):
            vdic[parId].add(src)
            vdic[parId].add(tar)
        else:
            vs = set()
            vs.add(src)
            vs.add(tar)
            vdic[parId] = vs

    overall = 0L
    for id, vs in vdic.iteritems():
        overall += len(vs)
    vs = set()
    for key, vertices in vdic.iteritems():
        vs.update(vertices)
    numOfVertices = len(vs)

    vrf = overall/float(numOfVertices)

    # to store/print the size of each partition
    sizeStr = ""
    for id, en in ndic.iteritems():
        sizeStr += str(en) + "\n"

    # the partitioning result(string)
    parRs = "*EP1D Partitioning*\n" + "Vertices: " + str(numOfVertices) + "\n" + "Edges: " + str(numOfEdges) + "\n" + \
             "Size of Each Partition: \n" + sizeStr + "Vertex Replica Factor: \n" + str(vrf)


    return partitions, [], parRs


# EdgePartition2D
def EP2D(edgesFile, numOfPar):
    f = open(edgesFile, "r")
    # a list to store the edges and their partition id
    # [(1, 10, {"partition": 2}), ...]
    partitions = []
    # the number of edges
    numOfEdges = 0
    # the number of vertices
    numOfVertices = 0

    # a dict to store the vertices in each partition
    vdic = {}
    # a dict to store the number of edges in each partition
    ndic = {}
    parRs = ""
    for line in f:
        numOfEdges += 1
        srcTar = line.strip().split()
        # a -> b  => a follows b ??
        src = long(srcTar[0])
        # src = long(srcTar[1])
        tar = long(srcTar[1])

        mixingPrime = 1125899906842597L
        #parId = int(abs(src * mixingPrime) % numOfPar)
        ceilSqrtNumParts = int(math.ceil(math.sqrt(numOfPar)))
        parId = -1
        if(numOfPar == ceilSqrtNumParts * ceilSqrtNumParts):
            col = int(abs(src * mixingPrime) % numOfPar)
            row = int(abs(tar * mixingPrime) % numOfPar)
            parId = (col * ceilSqrtNumParts + row) % numOfPar
        else:
            cols = ceilSqrtNumParts
            rows = (numOfPar + cols - 1) / cols
            lastColRows = numOfPar - rows * (cols - 1)
            col = int(abs(src * mixingPrime) % numOfPar / rows)
            row = -1
            if col < cols -1:
                row = int(abs(tar * mixingPrime) % rows)
            else:
                row = int(abs(tar * mixingPrime) % lastColRows)
            parId = col * rows + row



        dic1 = {}
        dic1["partition"] = parId
        partitions.append((src, tar, dic1))

        if ndic.has_key(parId):
            num = ndic[parId]
            ndic[parId] = num+1
        else:
            ndic[parId] = 1L

        if vdic.has_key(parId):
            vdic[parId].add(src)
            vdic[parId].add(tar)
        else:
            vs = set()
            vs.add(src)
            vs.add(tar)
            vdic[parId] = vs

    overall = 0L
    for id, vs in vdic.iteritems():
        overall += len(vs)
    vs = set()
    for key, vertices in vdic.iteritems():
        vs.update(vertices)
    numOfVertices = len(vs)

    vrf = overall/float(numOfVertices)

    # to store/print the size of each partition
    sizeStr = ""
    for id, en in ndic.iteritems():
        sizeStr += str(en) + "\n"

    # the partitioning result(string)
    parRs = "*EP2D Partitioning*\n" + "Vertices: " + str(numOfVertices) + "\n" + "Edges: " + str(numOfEdges) + "\n" + \
             "Size of Each Partition: \n" + sizeStr + "Vertex Replica Factor: \n" + str(vrf)


    return partitions, [], parRs



