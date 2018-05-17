#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from bidict import bidict

d = bidict({1:2})

print d
print d[1]
D = d.inv
print D
print D[2]
