#!/usr/bin/python
# -*- coding: utf-8 -*-

# the main program to create UI of Graph Partitioning Demostration

import RandomPartitioning
import RVCHashPartitioning
import CRVHashPartitioning
import EP1DHashPartitioning
import EP2DHashPartitioning
import PowerGraphPartitioning
import GreedyPartitioning
import GridPartitioning
import PDSPartitioning
import DBH1Partitioning
import DBH2Partitioning
import HDRFPartitioning
import CLDAPartitioning
import wjPartitioning

if __name__ == '__main__':
    
    file = "/home/w/data/Wiki-VoteRandom.txt"
    numOfPart = 100

    print "Random \n"
    RandomPartitioning.randomAL(file, numOfPart)
    print '\n'

    print "RVC \n"
    RVCHashPartitioning.RVChashAL(file, numOfPart)
    print '\n'

    print "CRV \n"
    CRVHashPartitioning.CRVhashAL(file, numOfPart)
    print '\n'

    print "EP1D \n"
    EP1DHashPartitioning.EP1DhashAL(file, numOfPart)
    print '\n'

    print "EP2D \n"
    EP2DHashPartitioning.EP2DhashAL(file, numOfPart)
    print '\n'

    print "PowerGraph \n"
    PowerGraphPartitioning.Greedy(file, numOfPart)
    print '\n'

    print "Greedy \n"
    GreedyPartitioning.GreedyAL(file, numOfPart)
    print '\n'
    
    print "Grid \n"
    GridPartitioning.GridAL(file, numOfPart)
    print '\n'

    print "PDS \n"
    PDSPartitioning.PDSAL(file, numOfPart)
    print '\n'

    print "DBH1 \n"
    DBH1Partitioning.DBH1AL(file, numOfPart)
    print '\n'

    print "DBH2 \n"
    DBH2Partitioning.DBH2AL(file, numOfPart)
    print '\n'

    print "HDRF \n"
    HDRFPartitioning.HDRFAL(file, numOfPart)
    print '\n'

    # print "CLDA \n"
    # CLDAPartitioning.CLDAAL(file, numOfPart)
    # print '\n'

    print "wj \n"
    wjPartitioning.wjAL(file, numOfPart)
    print '\n'


    