#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
to extract a smaller graph from large graph, using random picking...
Notice: the edge of two end-nodes without other linkage(in/out-degree is 0) would be discarded.

"""
import random

def graphExtract(edgesFile, ratio, output_file):

    ran = 100
    f = open(edgesFile, "r")
    w = open(output_file, "w")

    # to keep the out/in-degree of each vertex
    inOutDeg = {}

    # the list of edges
    edges = []

    # the list of refined edges
    refinedEdges = []

    for line in f:
        if random.uniform(0, ran) <= ran * ratio:
            #w.write(line)
            srcTar = line.strip().split()
            # a -> b  => a follows b ??
            src = long(srcTar[0])
            # src = long(srcTar[1])
            tar = long(srcTar[1])
            # tar = long(srcTar[0])


            edges.append((src, tar))

            # inOutDeg
            if inOutDeg.has_key(src):
                (inD, outD) = inOutDeg[src]
                inOutDeg[src] = (inD, outD + 1)
            else:
                inOutDeg[src] = (0, 1)

            if inOutDeg.has_key(tar):
                (inD, outD) = inOutDeg[tar]
                inOutDeg[tar] = (inD + 1, outD)
            else:
                inOutDeg[tar] = (1, 0)

    for e in edges:
        src_in = inOutDeg[e[0]][0]
        src_out = inOutDeg[e[0]][1]
        tar_in = inOutDeg[e[1]][0]
        tar_out = inOutDeg[e[1]][1]
        if (src_in + src_out) > 3 or (tar_in + tar_out) > 3:
            line = str(e[0])+"\t"+str(e[1])+"\n"
            w.write(line)


# the 2nd extractor using the vertex ID
def graphE2(edgesFile, maxVertexID, output_file):
    f = open(edgesFile, "r")
    w = open(output_file, "w")

    MIN = 1000
    MAX = MIN + maxVertexID
    for line in f:
        # w.write(line)
        srcTar = line.strip().split()
        # a -> b  => a follows b ??
        src = long(srcTar[0])
        # src = long(srcTar[1])
        tar = long(srcTar[1])
        if MIN <= src <= MAX and MIN <= tar <= MAX:
            w.write(line)





# test:
#graphExtract("./wiki-Vote.txt", 0.02, "./wikiVote_2k.txt")
graphE2("./wiki-Vote.txt", 500L, "./wikiVote_500L.txt")
