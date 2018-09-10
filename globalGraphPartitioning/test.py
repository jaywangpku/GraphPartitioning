#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.remove_edge(1, 2)
G.clear()

nx.draw(G)
plt.show()


