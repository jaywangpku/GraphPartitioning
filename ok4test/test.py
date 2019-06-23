#!/usr/bin/python
# -*- coding: utf-8 -*-

# 完整的hashing方案实现

import random
import math
import time

ans = 0
for i in range(1, 2):
    ans = ans + pow(i, -1.5)

print ans