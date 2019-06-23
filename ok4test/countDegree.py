#!/usr/bin/python
# -*- coding: utf-8 -*-

# 完整的hashing方案实现

import random
import math
import time

count = {}
ans = 0
vertex = set()
edge = 0
f = open("/home/w/data/Wiki-Vote-BFS1.txt", "r")
for line in f:
    edge = edge + 1
    srcTar = line.strip().split()
    if(srcTar[0] == '#'):
        continue
    src = long(srcTar[0])
    tar = long(srcTar[1])
    if count.has_key(src):
        count[src] = count[src] + 1
    else:
        count[src] = 1
    if count.has_key(tar):
        count[tar] = count[tar] + 1
    else:
        count[tar] = 1
    vertex.add(src)
    vertex.add(tar)

for k,v in count.items():
    if v == 1:
        ans = ans + 1

print ans
print edge
print len(vertex)

