#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
to get the track's details from RWtrack and Partitioning result

"""
import random

import os
import wx

def getTrackDetail(RWtrack, partitions, numOfPars):
    # to extract the partitions info of each vertex
    # : the ids of partition that vertex spans
    vPars = {}
    for x in partitions:
        srcV, tarV, parDic = x
        parID = parDic["partition"]
        if vPars.has_key(srcV):
            vPars[srcV].add(parID)
        else:
            vPars[srcV] = set([parID])
        if vPars.has_key(tarV):
            vPars[tarV].add(parID)
        else:
            vPars[tarV] = set([parID])

    # to calculate the track of Random Walk
    # a array list to store the result
    track = []
    for i in range(0, numOfPars):
        track.append([])

    for i in range(0, len(RWtrack)):
        v = RWtrack[i]
        parIDs = vPars[v]
        for x in range(0, numOfPars):
            pID = x+1
            if pID in parIDs:
                #track[x].append("Partition "+str(pID))
                track[x].append(pID)
            else:
                track[x].append(None)

    return track

'''
[
[None, None, None, None, "Partition 1", "Partition 1", "Partition 1", "Partition 1", None, None, None, None],
[None, None, None, None, None, None, None, None, None, "Partition 2", "Partition 2", "Partition 2"],
]
'''



