#!/usr/bin/python
# -*- coding: utf-8 -*-

# 用于将整个边集全部打乱

import random
import math
import time

def change2random(edgelist, numOfParts):
    f = open(edgelist, "r")
    fchange = open("/home/w/data/web-StanfordRandom.txt", "w+")
    lines = []
    for line in f:
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        lines.append((src, tar))
    order = []
    for i in range(len(lines)):
        order.append(i)
    for i in range(len(order)):
        j = random.randint(0, len(order) - 1)
        temp = order[i]
        order[i] = order[j]
        order[j] = temp
    for i in range(len(lines)):
        src = lines[order[i]][0]
        tar = lines[order[i]][1]
        s = str(src) + '\t' + str(tar) + '\n'
        fchange.write(s)
        
       
# time_start = time.time()

change2random("/home/w/data/web-Stanford.txt", 100000)

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

