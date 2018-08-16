#!/usr/bin/python
# -*- coding: utf-8 -*-

# 用于构造固定窗口大小下，滑动窗口带来的离散度增益

import random
import math
import time

def SWRdata(edgelist, numOfParts):
    f = open(edgelist, "r")
    fchange = open("/home/w/data/testdata/bfs1_70000_0.4.txt", "w+")
    lines = []
    afterlines = []
    for line in f:
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        lines.append((src, tar))
    window = 70000
    threshold = 0.4
    win = []
    line = 0
    while line < len(lines):
        while len(win) < window and line < len(lines):
            win.append(lines[line])
            line = line + 1
        order = []
        for i in range(len(win)):
            order.append(i)
        for i in range(len(order)):
            j = random.randint(0, len(order) - 1)
            temp = order[i]
            order[i] = order[j]
            order[j] = temp
        rmlen = int(len(order)*threshold)
        rmwin = set()
        for i in range(rmlen):
            src = win[order[i]][0]
            tar = win[order[i]][1]
            rmwin.add((src, tar))
            s = str(src) + '\t' + str(tar) + '\n'
            fchange.write(s)
        win = list(set(win)-rmwin)

    # 最后的部分边
    order = []
    for i in range(len(win)):
        order.append(i)
    for i in range(len(order)):
        j = random.randint(0, len(order) - 1)
        temp = order[i]
        order[i] = order[j]
        order[j] = temp
    for i in range(len(win)):
        src = win[order[i]][0]
        tar = win[order[i]][1]
        s = str(src) + '\t' + str(tar) + '\n'
        fchange.write(s)

    # 测试完成，代码没有问题
    # print len(lines), len(afterlines), len(list(set(lines)-set(afterlines)))



# time_start = time.time()

SWRdata("/home/w/data/testdata/bfs1.txt", 10)

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

