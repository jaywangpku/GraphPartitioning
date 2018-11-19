#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
the edge/vertex drawing function/class for partitioning graph using networkx library
Notice:
The functions in this file have been replaced by those in GraphDraw_plotly which uses plotly library.

"""

import networkx as nx
import numpy as np
import plotly
import plotly.plotly as py
from networkx.generators.atlas import *

# from networkx.algorithms.isomorphism.isomorph import graph_could_be_isomorphic as isomorphic
import random

import os
import wx

#plotly.tools.set_credentials_file(username='zhua1987', api_key='7tupnmzgj5')

edges = [(1, 10, {"block": 2}), (1, 4, {"block": 2}), (1, 7, {"block": 2}), (8, 7, {"block": 2}),
         (10, 2, {"block": 3}), (2, 3, {"block": 3}), (2, 5, {"block": 3}), (2, 6, {"block": 3})]

nodes = [(1, "s"), (2, "s"), (3, ""), (4, ""), (5, ""), (6, ""), (7, ""), (8, ""), (10, "")]

colors = ["g", "b", "cyan", "aliceblue", "antiquewhite", "aquamarine", "chartreuse", "brown", "coral", "gold",
          "darkgreen"]


def gDraw(edgelist, nodelist, colors, digName):

    #plotly.offline.init_notebook_mode()

    G = nx.Graph()
    G.add_edges_from(edgelist)

    # a dictionary to store these edges by their block id
    blocksDic = {}
    for e in edgelist:
        k = e[2]["block"]
        ev = (e[0], e[1])
        if blocksDic.has_key(k):
            blocksDic[k].append(ev)
        else:
            blocksDic[k] = [ev]

    # a list to store those seeds
    seeds = []
    for n in nodelist:
        if n[1] == "s":
            seeds.append(n[0])

    # a list to store other normal vertices
    otherVertices = []
    for n in nodes:
        otherVertices.append(n[0])
    for s in seeds:
        otherVertices.remove(s)

    import matplotlib.pyplot as plt
    # pos=nx.spring_layout(G) # positions for all nodes

    # position is stored as node attribute data for random_geometric_graph
    # pos=nx.get_node_attributes(G,'pos')

    # layout graphs with positions using graphviz neato
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
    #pos = graphviz_layout(G, prog="neato")
    pos=nx.spectral_layout(G)

    plt.figure(figsize=(8, 8))

    # nodes
    # draw the seeds in red color
    nx.draw_networkx_nodes(G, pos,
                           nodelist=seeds,
                           node_color='r',
                           node_size=50,
                           alpha=0.8)
    # draw other vertices in pink color
    nx.draw_networkx_nodes(G, pos,
                           nodelist=otherVertices,
                           node_color='pink',
                           node_size=50,
                           alpha=0.8)

    # edges
    # nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
    i = 0
    for key in blocksDic.keys():
        nx.draw_networkx_edges(G, pos,
                               edgelist=blocksDic[key],
                               width=3, alpha=0.5, edge_color=colors[i])
        i = i + 1

    # nx.draw(G)

    #plt.axis('off')
    plt.savefig(digName + ".png")
    plt.show()

    #fig = plt.figure()
    plt.axis('off')
    fig = plt.gcf()

    pu = plotly.offline.plot_mpl(fig, auto_open=False)
    #plot_url = py.iplot_mpl(fig)
    print pu



# gDraw(edges, nodes, colors)


"""

G=nx.Graph()

edgeDis = (1, 10, {"block":2})

print edgeDis

G.add_edge(*edgeDis)

G.add_edge(1, 4, {"block":2})
G.add_edge(1, 7, {"block":2})

G.add_edge(10, 2, {"block":3})
G.add_edge(2, 3, {"block":3})
G.add_edge(2, 5, {"block":3})
G.add_edge(2, 6, {"block":3})

#print G.nodes()
#print G.edges()
#print G.neighbors(1)
print G[1]

import matplotlib.pyplot as plt
#pos=nx.spring_layout(G) # positions for all nodes

# position is stored as node attribute data for random_geometric_graph
#pos=nx.get_node_attributes(G,'pos')

# layout graphs with positions using graphviz neato
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout
pos = graphviz_layout(G, prog="neato")

plt.figure(figsize=(8,8))

# nodes
nx.draw_networkx_nodes(G,pos,
                       nodelist=[1,2],
                       node_color='r',
                       node_size=50,
               alpha=0.8)

nx.draw_networkx_nodes(G,pos,
                       nodelist=[3,4,5,6,7,10],
                       node_color='pink',
                       node_size=50,
               alpha=0.8)

# edges
#nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)

nx.draw_networkx_edges(G,pos,
                       edgelist=[(1,10),(1,4),(1,7)],
                       width=3,alpha=0.5,edge_color='g')
nx.draw_networkx_edges(G,pos,
                       edgelist=[(2,3), (2,5), (2,6),(10,2)],
                       width=3,alpha=0.5,edge_color='b')

#nx.draw(G)
plt.axis('off')
plt.savefig("draw.png")
plt.show()

"""
