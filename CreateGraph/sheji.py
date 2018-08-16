#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

y = [1,11,14,28,66,166,333,540,620,705,742,3153,5947,8497,10938,13630,15719,17622,19641]
x = [1,5000,10000,20000,30000,40000,50000,60000,70000,80000,100000,300000,500000,700000,900000,1100000,1300000,1500000,1699711]
for i in range(len(x)):
	x[i] = x[i] /1.0/ 1699711
for i in range(len(x)):
	if x[i] <= 0.05:
		x[i] = x[i]/0.01*0.1
	else:
		x[i] = (x[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y)):
	if y[i] <= 1000:
		y[i] = y[i]/200.0 * 2000
	else:
		y[i] = (y[i] - 1000)/1.0/4000*2000+10000

x1 = [20000,20000,20000,20000]
y1 = [28,50,77,114]
for i in range(len(x1)):
	x1[i] = x1[i] /1.0/ 1699711
for i in range(len(x1)):
	if x1[i] <= 0.05:
		x1[i] = x1[i]/0.01*0.1
	else:
		x1[i] = (x1[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y1)):
	if y1[i] <= 1000:
		y1[i] = y1[i]/200.0 * 2000
	else:
		y1[i] = (y1[i] - 1000)/1.0/4000*2000+10000

x2 = [30000,30000,30000,30000]
y2 = [66,121,178,284]
for i in range(len(x1)):
	x2[i] = x2[i] /1.0/ 1699711
for i in range(len(x2)):
	if x2[i] <= 0.05:
		x2[i] = x2[i]/0.01*0.1
	else:
		x2[i] = (x2[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y2)):
	if y2[i] <= 1000:
		y2[i] = y2[i]/200.0 * 2000
	else:
		y2[i] = (y2[i] - 1000)/1.0/4000*2000+10000

x3 = [40000,40000,40000,40000]
y3 = [166,235,355,438]
for i in range(len(x3)):
	x3[i] = x3[i] /1.0/ 1699711
for i in range(len(x3)):
	if x3[i] <= 0.05:
		x3[i] = x3[i]/0.01*0.1
	else:
		x3[i] = (x3[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y3)):
	if y3[i] <= 1000:
		y3[i] = y3[i]/200.0 * 2000
	else:
		y3[i] = (y3[i] - 1000)/1.0/4000*2000+10000

x4 = [50000,50000,50000,50000]
y4 = [333,418,498,609]
for i in range(len(x4)):
	x4[i] = x4[i] /1.0/ 1699711
for i in range(len(x4)):
	if x4[i] <= 0.05:
		x4[i] = x4[i]/0.01*0.1
	else:
		x4[i] = (x4[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y4)):
	if y4[i] <= 1000:
		y4[i] = y4[i]/200.0 * 2000
	else:
		y4[i] = (y4[i] - 1000)/1.0/4000*2000+10000

x5 = [60000,60000,60000,60000]
y5 = [540,622,660,750]
for i in range(len(x5)):
	x5[i] = x5[i] /1.0/ 1699711
for i in range(len(x5)):
	if x5[i] <= 0.05:
		x5[i] = x5[i]/0.01*0.1
	else:
		x5[i] = (x5[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y5)):
	if y5[i] <= 1000:
		y5[i] = y5[i]/200.0 * 2000
	else:
		y5[i] = (y5[i] - 1000)/1.0/4000*2000+10000

x6 = [70000,70000,70000,70000]
y6 = [620, 685, 733,786]
for i in range(len(x6)):
	x6[i] = x6[i] /1.0/ 1699711
for i in range(len(x6)):
	if x6[i] <= 0.05:
		x6[i] = x6[i]/0.01*0.1
	else:
		x6[i] = (x6[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y6)):
	if y6[i] <= 1000:
		y6[i] = y6[i]/200.0 * 2000
	else:
		y6[i] = (y6[i] - 1000)/1.0/4000*2000+10000

x7 = [80000,80000,80000,80000]
y7 = [705,739,774,854]
for i in range(len(x7)):
	x7[i] = x7[i] /1.0/ 1699711
for i in range(len(x4)):
	if x7[i] <= 0.05:
		x7[i] = x7[i]/0.01*0.1
	else:
		x7[i] = (x7[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y7)):
	if y7[i] <= 1000:
		y7[i] = y7[i]/200.0 * 2000
	else:
		y7[i] = (y7[i] - 1000)/1.0/4000*2000+10000


x9 = [100000,100000,100000,100000]
y9 = [742,820,874,990]
for i in range(len(x7)):
	x9[i] = x9[i] /1.0/ 1699711
for i in range(len(x4)):
	if x9[i] <= 0.05:
		x9[i] = x9[i]/0.01*0.1
	else:
		x9[i] = (x9[i] - 0.05)/0.2*0.1+0.5

for i in range(len(y9)):
	if y9[i] <= 1000:
		y9[i] = y9[i]/200.0 * 2000
	else:
		y9[i] = (y9[i] - 1000)/1.0/4000*2000+10000



plt.xticks((0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1),('0','0.01','0.02','0.03','0.04','0.05','0.2','0.4','0.6','0.8','1'))
plt.yticks((0,2000,4000,6000,8000,10000,12000,14000,16000,18000,20000),('0','200','400','600','800','1000','4000','8000','12000','16000','20000'))

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.xlabel("Window size", fontsize=16)
plt.ylabel("Dispersion factor", fontsize=16)




plt.xlim(0,1)
plt.ylim(0,20000)






xx = []
yy = []
for i in range(40):
	yy.append(250*i)
	xx.append(0.5)
plt.scatter(xx, yy, marker = 'o', s = 1, color = 'black', alpha = 1.0)

xxx = []
yyy = []
for i in range(50):
	xxx.append(0.01*i)
	yyy.append(10000)
plt.scatter(xxx, yyy, marker = 'o', s = 1, color = 'black', alpha = 1.0)


# plt.xticks((0,20,40,60,80,100,120),('200504','200912','201108','201306','201502','201610',''))

b = 0.5

plt.plot(x, y, marker = '^', color = 'blue', alpha = b)
plt.plot(x1, y1, marker = 'o', color = 'red', alpha = b)
plt.plot(x2, y2, marker = 'o', color = 'red', alpha = b)
plt.plot(x3, y3, marker = 'o', color = 'red', alpha = b)
plt.plot(x4, y4, marker = 'o', color = 'red', alpha = b)
plt.plot(x5, y5, marker = 'o', color = 'red', alpha = b)
plt.plot(x6, y6, marker = 'o', color = 'red', alpha = b)
plt.plot(x7, y7, marker = 'o', color = 'red', alpha = b)
plt.plot(x9, y9, marker = 'o', color = 'red', alpha = b)
plt.show()