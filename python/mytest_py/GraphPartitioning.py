#!/usr/bin/python
# -*- coding: utf-8 -*-

# the main program to create UI of Graph Partitioning Demostration

import os
import RandomPartitioning
import PowerGraphPartitioning
import BlockPartitioning

if __name__ == '__main__':
    file = "/home/w/data/Wiki-Vote.txt"
    numOfPart = 4

    Partitions, ans = RandomPartitioning.RVC(file, numOfPart)
    print ans, "\n"
    
    Partitions, ans = RandomPartitioning.CRV(file, numOfPart)
    print ans, "\n"

    Partitions, ans = RandomPartitioning.EP1D(file, numOfPart)
    print ans, "\n"

    Partitions, ans = RandomPartitioning.EP2D(file, numOfPart)
    print ans, "\n"

    Partitions, ans = PowerGraphPartitioning.PowerGraphPar(file, numOfPart)
    print ans, "\n"

    # (edgesFile, numOfPars, numOfBlocks, tel, depthOfBFS, lowerBound, UpperBound)
    Partitions,nodes, ans = BlockPartitioning.blockPartition(file, numOfPart, 10 * numOfPart, 0.2, 5, 0.8, 1.2)
    print ans, "\n"