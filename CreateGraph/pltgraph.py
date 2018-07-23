#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import networkx as nx

G = nx.Graph()
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(1,4)
G.add_edge(1,5)
G.add_edge(1,6)
G.add_edge(1,7)
G.add_edge(1,8)
G.add_edge(1,9)
G.add_edge(2,5)
G.add_edge(4,9)
G.add_edge(8,3)
G.add_edge(2,7)
G.add_edge(7,9)

nx.draw(G, pos=nx.spring_layout(G), node_color = 'r', edge_color = 'b', with_labels = True, font_size = 22, node_size = 3000)
plt.show()