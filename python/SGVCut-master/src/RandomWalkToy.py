#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
a function to simulate a random walk given the length of walk
NOTICE: the starting vertex is set randomly.
'''

import os
import random

def randomWalk(edgesFile, lengthOfWalk):

    # the starting vertex
    starV = 0L

    # a set of vertices
    vertices = set()

    # a dictionary to store those out-linkages
    # {(src, [tar1, tar2, ...]), ...}
    vertexOutLinks = {}

    # a dictionary to store the visit times to each vertex
    visTimes = {}

    # the number of vertices
    numOfVer = 0L

    # the number of edges
    numOfEdg = 0L


    # to parse the edge list file to construct the containers above
    f = open(edgesFile, "r")
    for line in f:
        srcTar = line.strip().split()
        # a -> b  => a follows b ??
        src = long(srcTar[0])
        # src = long(srcTar[1])
        tar = long(srcTar[1])
        # tar = long(srcTar[0])

        # vertices
        vertices.add(src)
        vertices.add(tar)

        # to initialize the visit times to vertices
        visTimes[src] = 0
        visTimes[tar] = 0

        # vertexOutLinks,
        if vertexOutLinks.has_key(src):
            vertexOutLinks[src].append(tar)
        else:
            vertexOutLinks[src] = [tar]

    verList = list(vertices)
    starV = random.choice(verList)
    RWtrack = []

    for i in range(0, lengthOfWalk):
        RWtrack.append(starV)
        num = visTimes[starV]
        visTimes[starV] = num + 1
        if starV not in vertexOutLinks:
            starV = random.choice(verList)
        else:
            starV = random.choice(vertexOutLinks[starV])


    f.close()

    # an example
    #print visTimes[2]

    return visTimes, starV, RWtrack




