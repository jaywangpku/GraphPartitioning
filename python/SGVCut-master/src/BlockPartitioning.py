#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
our block-based edge partitioning method

"""

# import networkx as nx
# from networkx.generators.atlas import *
# from networkx.algorithms.isomorphism.isomorph import graph_could_be_isomorphic as isomorphic
import random

import os
import wx

# blocks splitting??
# Notice: here we don't introduce blocks splitting
# we select seeds using sum in and out-degree, and no any pair of seeds is connected directly.

def blockPartition(edgesFile, numOfPars, numOfBlocks, tel, depthOfBFS, lowerBound, UpperBound):
    
    # a list to store those seeds(vertices)
    seeds = []

    # a set of vertices
    vertices = set()
    
    # to keep the out/in-degree of each vertex
    inOutDeg = {}
    
    # a dictionary to store those linkages(in and out)
    vertexLinks = {}
    
    # a dictionary to store vertices and their distance values to each seed
    # e.g. {v_id:{1L:120.4, -2L:{} ...}, ...}
    # NOTICE here!
    # -2L:{} => added distance values in last calculation(superstep) to current vertex
    verDisVals = {}
    
    # a dictionary to store edges and their distance values to each seed
    # notice that here we keep only the seed with max value since we will NOT introduce block splitting in this demo
    # NOT used!
    edgeDisVals = {}

    # the list of edges
    edgesList = []
    
    # the initial distance value for seeds
    iniDisVal = 10000.0

    # a dict to store the blocks, {seed:[edges], ...}
    # notice that here an special block(seed_id: -1L) in which the edges are not allocated to any block
    blocks = {}

    # average size of a partition
    # aveSize = len(edgesList)/numOfPars

    # Vertex Replica Factor
    vrf = 0.0

    # the number of vertices
    numOfVer = 0L

    # the number of edges
    numOfEdg = 0L

    # the size of each partition
    sizeOfPar = []

    # to parse the edge list file to construct the containers above
    f = open(edgesFile, "r")
    for line in f:
        srcTar = line.strip().split()
        # a -> b  => a follows b ??
        src = long(srcTar[0])
        #src = long(srcTar[1])
        tar = long(srcTar[1])
        #tar = long(srcTar[0])

        # vertices
        vertices.add(src)
        vertices.add(tar)
        
        #inOutDeg
        if inOutDeg.has_key(src):
            (inD, outD) = inOutDeg[src]
            inOutDeg[src] = (inD, outD+1)
        else:
            inOutDeg[src] = (0, 1)
        
        if inOutDeg.has_key(tar):
            (inD, outD) = inOutDeg[tar]
            inOutDeg[tar] = (inD+1, outD)
        else:
            inOutDeg[tar] = (1, 0)
        
        
        #vertexLinks, (inVertices, outVertices)
        if vertexLinks.has_key(src):
            vertexLinks[src][1].append(tar)
        else:
            vertexLinks[src] = ([],[tar])

        if vertexLinks.has_key(tar):
            vertexLinks[tar][0].append(src)
        else:
            vertexLinks[tar] = ([src], [])
        
        # verDisVals
        for x in srcTar:
            verDisVals[long(x)] = {}
            verDisVals[long(x)][-2L] = {}

        
        # edgeDisVals
        #edgeDisVals[(src, tar)] = {}

        # edgesList
        edgesList.append((src, tar))

    # to sort the vertices on degree
    allDegs = []
    for key in inOutDeg.keys():
        (inD, outD) = inOutDeg[key]
        allDegs.append((key, inD+outD))
    def getKey(item):
        return item[1]
    sortedAllDegs = sorted(allDegs, key=getKey, reverse=True)

    # an iterator of sortedAllDegs
    di = iter(sortedAllDegs)
    # select the first seed
    firstSeed = di.next()[0]
    seeds.append(firstSeed)
    # a set to keep the directly connected vertices of current seeds
    dirVertices = set(vertexLinks[firstSeed][0] + vertexLinks[firstSeed][1])

    # the number of selected seeds should be equal to numOfBlocks
    while len(seeds) < numOfBlocks:
        nx = -1L
        try:
            nx = di.next()[0]
        except StopIteration:
            break
        if nx not in dirVertices:
            seeds.append(nx)
            dirVertices.update(vertexLinks[nx][0] + vertexLinks[nx][1])

    # to initialize the distance value for each seed vertex to itself
    for s in seeds:
        #vdic = {}
        #vdic[s] = iniDisVal
        verDisVals[s][s] = iniDisVal
        verDisVals[s][-2L] = {s: iniDisVal}

    # to calculate and send the distance values for each vertex, from seeds
    for i in range(0, depthOfBFS):
        # a dict to store the messages sent, {tarV:{},...}
        mesgs = {}
        for key, vals in verDisVals.iteritems():
            # the out vertices of key
            # for undirected graph, e.g. facebook_combined.txt
            #tars = vertexLinks[key][0] + vertexLinks[key][1]
            # for directed graph:
            tars = vertexLinks[key][1]
            outd = len(tars)
            #print "tars: ", tars
            if vals.has_key(-2L) and vals[-2L] and outd > 0:
                # a temp dict to store the messages sent from current vertex
                tdic = {}
                for sd, va in vals[-2L].iteritems():
                    #print sd, va
                    tdic[sd] = (va/outd)*tel
                #print "tdic: ", tdic
                for ov in tars:
                    if mesgs.has_key(ov):
                        for s, v in tdic.iteritems():
                            if mesgs[ov].has_key(s):
                                old = mesgs[ov][s]
                                mesgs[ov][s] = old + v
                            else:
                                mesgs[ov][s] = v
                    else:
                        mesgs[ov] = tdic
                vals[-2L].clear()

        # to add the new distance values(in messages) to current vertex
        #print "mesgs", mesgs
        for tar, vals in mesgs.iteritems():
            del verDisVals[tar][-2L]
            #print "vals: ", vals
            #print "verDisVals[tar]: ", verDisVals[tar]
            if verDisVals[tar]:
                old = verDisVals[tar]
                for s, v in vals.iteritems():
                    if old.has_key(s):
                        curr = old[s]
                        old[s] = curr + v
                    else:
                        old[s] = v
                #verDisVals[tar][-2L].clear()
                verDisVals[tar][-2L] = vals
            else:
                tmp = vals.copy()
                verDisVals[tar] = tmp
                verDisVals[tar][-2L] = vals

            #print "-2L: ", verDisVals[tar][-2L]

    # to sum the distance values of two end vertices for each edge
    # firstly, a func to sum two dictionaries
    def sumDicts(dict1, dict2):
        dic = dict2.copy()
        for key, val in dict1.iteritems():
            if dic.has_key(key):
                old = dic[key]
                dic[key] = old + val
            else:
                dic[key] = val
        return dic

    # secondly, a func to extract the seed with max distance value for every edge!
    def maxSeed(EdgeVals):
        seed = -1L
        maxV = 0.0
        for s, v in EdgeVals.iteritems():
            if v > maxV:
                seed = s
                maxV = v
        if seed != -1L:
            return seed

    for src, tar in edgesList:
        srcDic = verDisVals[src]
        if srcDic.has_key(-2L):
            del srcDic[-2L]
        tarDic = verDisVals[tar]
        if tarDic.has_key(-2L):
            del tarDic[-2L]

        sumD = sumDicts(srcDic, tarDic)
        if sumD:
            sd = maxSeed(sumD)
            if blocks.has_key(sd):
                blocks[sd].append((src, tar))
            else:
                blocks[sd] = [(src, tar)]

        else:
            if blocks.has_key(-1L):
                blocks[-1L].append((src, tar))
            else:
                blocks[-1L] = [(src, tar)]

    print "num of seeds: ", len(seeds)
    #print "seeds: ", seeds


    # to make blocks merging
    # to construct a list of blocks' size
    blockSizes = []
    for sd, edges in blocks.iteritems():
        blockSizes.append((sd, len(edges)))
        #print "seed:", sd, "; ", "edges: ", edges

    # to sort the block-sizes list in descending order
    sortedBS = sorted(blockSizes, key=getKey, reverse=True)
    print "size of sortedBS: ", len(sortedBS)
    #print sortedBS
    #iBS = iter(sortedBS)

    # a list of size numOfPars to store the merging result, [(sizeOfPar, [blocks]),...]
    # WRONG:
    #mergingRs = [(0L, [])] * numOfPars
    mergingRs = [(0L, [])]
    for i in range(1, numOfPars):
        mergingRs.append((0L, []))
    idx_merge = 0
    min_size = 0L
    for sd, bsize in sortedBS:
        print sd, ":", bsize
        if sd != -1L:
            print "the out/in degrees:", inOutDeg[sd]
        #old = mergingRs[idx_merge][0]
        mergingRs[idx_merge] = (min_size + bsize, mergingRs[idx_merge][1])
        mergingRs[idx_merge][1].append(sd)
        min_size += bsize
        for i in range(0, len(mergingRs)):
            newSize = mergingRs[i][0]
            if newSize < min_size:
                min_size = newSize
                idx_merge = i

    # a list to store the edges and their partition id
    # [(1, 10, {"partition": 2}), ...]
    partitions = []
    parID = 1
    for x in mergingRs:
        #print x[0], x[1]
        for b in x[1]:
            edges = blocks[b]
            for e in edges:
                dic1 = {}
                dic1["partition"] = parID
                partitions.append((e[0], e[1], dic1))
        parID += 1

    # a list to store nodes and indicator of seed
    nodes = []
    for v in vertices:
        if v in seeds:
            nodes.append((v, "s"))
        else:
            nodes.append((v, ""))

    # to store/print the size of each partition
    sizeStr = ""
    for x in mergingRs:
        sizeOfPar.append(x[0])
        sizeStr += str(x[0]) + "\n"
        print x[0]
    #for x in partitions:
    #    print x
    #print len(partitions)

    numOfVer = len(verDisVals)
    numOfEdg = len(edgesList)

    # to calculate the Vertex Replica Factor
    overrall = 0L
    for sibs in mergingRs:
        vset = set([])
        for b in sibs[1]:
            for edge in blocks[b]:
                vset.add(edge[0])
                vset.add(edge[1])
        overrall += len(vset)

    vrf = (overrall/float(numOfVer))

    # the partitioning result(string)
    pr = "*Blocked Partitioning*\n" + "Vertices: " + str(numOfVer) + "\n" + "Edges: " + str(numOfEdg) + "\n" + \
         "Size of Each Partition: \n" + sizeStr + "Vertex Replica Factor: \n" + str(vrf)

    return partitions, nodes, pr










