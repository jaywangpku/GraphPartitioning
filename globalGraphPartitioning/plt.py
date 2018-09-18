#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt

# 绘制直方图
# name_list = ["NE", "SWR", "HDRF"]
# num1_list = [3.56, 5.64, 6.97]
# num2_list = [32.957, 0.85, 9.86]
# index = [0,1,2]
# rects = plt.bar(range(3), num2_list, color="rgb")
# plt.ylim(ymax=40, ymin=0)
# plt.xticks(index, name_list)
# plt.ylabel("TIME")
# for rect in rects:
# 	height = rect.get_height()
# 	plt.text(rect.get_x() + rect.get_width()/2.0, height, str(height), ha="center", va="bottom")
# plt.show()

# 绘制折线图
x = [4, 8, 16, 32, 64, 100]
y1 = [1.34, 1.61, 1.99, 2.49, 3.09, 3.56]
y2 = [1.75, 2.39, 3.16, 4.067, 5.004, 5.64]
y3 = [1.89, 2.68, 3.74, 4.82, 6.24, 6.97]
y4 = [32, 32, 32, 32, 32, 32]
y5 = [0.63, 0.69, 0.72, 0.84, 0.83, 0.85]
y6 = [0.71, 1.14, 1.97, 3.48, 6.69, 9.86]
plt.plot(x, y1, marker='o', mec='r', mfc='w', label="$NE$")
plt.plot(x, y2, marker='*', mec='r', mfc='w', label="$SWR$")
plt.plot(x, y3, marker='+', mec='r', mfc='w', label="$HDRF$")
plt.xlabel("Numbers")
plt.ylabel("VRF")
plt.legend()
plt.show()