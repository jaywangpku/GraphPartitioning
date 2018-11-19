#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

f = open("/home/w/mytest/wjalgorithm/ans1.txt", "r")
x = []
y = []
for line in f:
	ans = line.strip().split()
	fans = float(ans[0])
	y.append(fans)
for i in range(len(y)):
	x.append(i)

xx = []
yy = []
for i in range(len(y)):
	if i % 10 == 0:
		if y[i] < 100000:
			yy.append(y[i])
for i in range(len(yy)):
	xx.append(i)
print yy

plt.scatter(xx, yy, marker = 'o', s = 1, color = 'blue', alpha = 0.3)
plt.show()