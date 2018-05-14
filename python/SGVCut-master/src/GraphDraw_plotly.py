#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
the edge/vertex drawing function/class for partitioning graph using Plotly/networkx library

"""

import networkx as nx
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF

import plotly.plotly as py
from networkx.generators.atlas import *

# from networkx.algorithms.isomorphism.isomorph import graph_could_be_isomorphic as isomorphic
import random

import os
import wx

import BlockPartitioning

#plotly.tools.set_credentials_file(username='zhua1987', api_key='7tupnmzgj5')

edges = [(1, 10, {"partition": 2}), (1, 4, {"partition": 2}), (1, 7, {"partition": 2}), (8, 7, {"partition": 2}),
         (10, 2, {"partition": 3}), (2, 3, {"partition": 3}), (2, 5, {"partition": 3}), (2, 6, {"partition": 3})]

nodes = [(1, "s"), (2, "s"), (3, ""), (4, ""), (5, ""), (6, ""), (7, ""), (8, ""), (10, "")]

colors = ["g", "cyan", "chartreuse", "brown", "coral", "gold",
          "darkgreen"]


def gDraw(edgelist, nodelist, colors, digName):

    #plotly.offline.init_notebook_mode()

    g = nx.Graph()
    g.add_edges_from(edgelist)

    # a dictionary to store these edges by their partition id
    partitionsDic = {}

    for e in edgelist:
        k = e[2]["partition"]
        ev = (e[0], e[1])
        if partitionsDic.has_key(k):
            partitionsDic[k].append(ev)
        else:
            partitionsDic[k] = [ev]

        # a dict to store the replica factor of each vertex
        verRF = {}
        verSets = []
        for bid, edges in partitionsDic.iteritems():
            tset = set()
            for x in edges:
                tset.add(x[0])
                tset.add(x[1])
            verSets.append(tset)
        for vset in verSets:
            for ver in vset:
                if verRF.has_key(ver):
                    rf = verRF[ver]
                    verRF[ver] = rf + 1
                else:
                    verRF[ver] = 1

    #partitionsDic = edgelist
    #for k, v in partitionsDic.iteritems():
    #    print k, len(v)

    # a list to store those seeds
    seeds = []
    # a list to store other normal vertices
    otherVertices = []

    for n in nodelist:
        if n[1] == "s":
            seeds.append(n[0])
        else:
            otherVertices.append(n[0])


    #import matplotlib.pyplot as plt

    #pos=nx.spring_layout(g) # positions for all nodes

    # position is stored as node attribute data for random_geometric_graph
    #pos=nx.get_node_attributes(g,'pos')

    # layout graphs with positions using graphviz neato
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
    #pos = graphviz_layout(g, prog="sfdp")
    pos = graphviz_layout(g, prog="neato")
    #pos = nx.fruchterman_reingold_layout(g)
    #pos=nx.spectral_layout(g)


    # to get the positions of seeds
    seeds_Xv = []
    seeds_Yv = []
    for s in seeds:
        if pos.has_key(s):
            seeds_Xv.append(pos[s][0])
            seeds_Yv.append(pos[s][1])

    # to get the positions of other normal vertices
    nor_Xv = []
    nor_Yv = []
    for s in otherVertices:
        if pos.has_key(s):
            nor_Xv.append(pos[s][0])
            nor_Yv.append(pos[s][1])

    # a list to store the names of seeds
    seedNms = []
    for i in range(len(seeds)):
        seedNms.append("seed_"+str(i+1))


    # the trace of seeds
    trace_vs = go.Scatter(x=seeds_Xv,
                        y=seeds_Yv,
                        xaxis='x2',
                        yaxis='y2',
                        mode='markers',
                        name='Seeds',
                        marker=go.Marker(symbol='dot',
                                        size=10,
                                        # color='#e1441c',
                                        line=go.Line(color='rgb(50,50,50)', width=0.6)
                                        ),
                        text=seedNms,
                        hoverinfo='text'
                        )

    # the trace of other vertices
    trace_ov = go.Scatter(x=nor_Xv,
                        y=nor_Yv,
                        xaxis='x2',
                        yaxis='y2',
                        mode='markers',
                        name='Normal Vertices',
                        hoverinfo='none',
                        marker=go.Marker(symbol='dot',
                                        size=2,
                                        # color='#6959CD',
                                        line=go.Line(color='rgb(50,50,50)', width=0.2)
                                        ),
                        )

    # the trace of other vertices
    trace_ov = go.Scatter(x=nor_Xv,
                        y=nor_Yv,
                        xaxis='x2',
                        yaxis='y2',
                        mode='markers',
                        name='Normal Vertices',
                        hoverinfo='none',
                        marker=go.Marker(symbol='dot',
                                        size=2,
                                        # color='#6959CD',
                                        line=go.Line(color='rgb(50,50,50)', width=0.2)
                                        ),
                        )

    # the list of datas for plotting
    ds = []
    col = 100
    i = 0
    for key, val in partitionsDic.iteritems():
        block_id = "partition_" + str(key)
        Xed = []
        Yed = []
        # parNames = []
        for edge in val:
            Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
            Yed += [pos[edge[0]][1], pos[edge[1]][1], None]
            # tep = block_id
            # parNames.append(tep)

        # col = col+30
        # scol = str(col)
        # rgbcol = "rgb("+scol+","+scol+","+scol+")"
        # hoinfo = [block_id] * len(val)
        trace = go.Scatter(x=Xed,
                        y=Yed,
                        xaxis='x2',
                        yaxis='y2',
                        mode='lines',
                        name=block_id,
                        # text=parNames,
                        # hoverinfo='text',
                        hoverinfo='name',
                        # line=go.Line(color=colors[i], width=2),
                        line=go.Line(width=2),
                        )
        i = i + 1
        ds.append(trace)

    ds.append(trace_vs)
    ds.append(trace_ov)

    """
    # the trace of seeds
    trace_vs = go.Scatter(x=seeds_Xv,
                          y=seeds_Yv,
                          mode='markers',
                          name='Seeds',
                          marker=go.Marker(symbol='dot',
                                           size=10,
                                           #color='#e1441c',
                                           line=go.Line(color='rgb(50,50,50)', width=0.6)
                                           ),
                          text=seedNms,
                          hoverinfo='text'
                          )

    # the trace of other vertices
    trace_ov = go.Scatter(x=nor_Xv,
                          y=nor_Yv,
                          mode='markers',
                          name='Normal Vertices',
                          marker=go.Marker(symbol='dot',
                                           size=2,
                                           #color='#6959CD',
                                           line=go.Line(color='rgb(50,50,50)', width=0.2)
                                           ),
                          )

    # the list of datas for plotting
    ds = []
    col = 100
    i = 0
    for key, val in partitionsDic.iteritems():
        block_id = "partition_" + str(key)
        Xed = []
        Yed = []
        for edge in val:
            Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
            Yed += [pos[edge[0]][1], pos[edge[1]][1], None]
        #col = col+30
        #scol = str(col)
        #rgbcol = "rgb("+scol+","+scol+","+scol+")"
        #hoinfo = [block_id] * len(val)
        trace = go.Scatter(x=Xed,
                           y=Yed,
                           mode='lines',
                           name=block_id,
                           #line=go.Line(color=colors[i], width=2),
                           line=go.Line(width=2),
                           )
        i = i+1
        ds.append(trace)

    ds.append(trace_vs)
    ds.append(trace_ov)
    """
    data1 = go.Data(ds)


    """
    Test:
    """
    # to get the sizes of partitions
    sizes = ""
    for bid, par in partitionsDic.iteritems():
        sizes += str(len(par))+", "
    # to calculate the VRF
    overallRF = 0
    for vset in verSets:
        overallRF += len(vset)
    vrf = overallRF/float(len(verRF))
    # Add table data
    table_data = [['Term', 'Result'],
                  ['Number of Vertices', str(len(verRF))],
                  ['Number of Edges', str(len(edgelist))],
                  #['Number of Blocks(for our method)', '...'],
                  ['Sizes of Partitions', sizes],
                  ['Vertex Replica Factor(VRF)', str(vrf)],
                  ]
    # Initialize a figure with FF.create_table(table_data)
    #font = ['#FCFCFC','#000000','#000000','#000000','#000000', '#FF3030', '#0099ff','#0099ff']
    font = ['#FCFCFC', '#000000', '#000000', '#000000', '#FF3030']
    figure = FF.create_table(table_data, font_colors=font)

    # Add trace data to figure
    figure['data'].extend(data1)

    # Edit layout for subplots
    figure.layout.yaxis.update({'domain': [0, .25]})
    figure.layout.yaxis2.update({'domain': [.3, 1]})
    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    figure.layout.yaxis2.update({'anchor': 'x2'})
    figure.layout.xaxis2.update({'anchor': 'y2'})
    #figure.layout.yaxis.update({'title': 'The Results of Partitioning and Random Walk Application'})
    # Update the margins to add a title and see graph x-labels.
    figure.layout.margin.update({'t': 75, 'l': 50})
    #figure.layout.update({'title': '2016 Hockey Stats'})
    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    figure.layout.update({'height': 800})

    pu = plotly.offline.plot(figure, auto_open=False, filename=digName + ".html")
    #fig1 = go.Figure(data=data1)
    #pu = plotly.offline.plot(fig1, auto_open=False, filename=digName+".html")



    print "pu: ", pu
    return pu


#parRs = BlockPartitioning.blockPartition("./soc-Slashdot0811.txt", 5, 80, 0.2, 4, 0.8, 1.2)
#gDraw(parRs[0], parRs[1], colors, "socSla0811_plotly")

#parRs = BlockPartitioning.blockPartition("./data_test", 3, 6, 0.2, 4, 0.8, 1.2)
#print "VRF: ", parRs[2]

#parRs = BlockPartitioning.blockPartition("./facebook_combined.txt", 5, 40, 0.2, 4, 0.8, 1.2)
#gDraw(parRs[0], parRs[1], colors, "facebook_Blocked")

#parRs = BlockPartitioning.blockPartition("./wiki-Vote.txt", 5, 80, 0.2, 4, 0.8, 1.2)
#gDraw(parRs[0], parRs[1], colors, "wikiVote_plotly")

#parRs = BlockPartitioning.blockPartition("./wikiVote_500L.txt", 3, 30, 0.2, 4, 0.8, 1.2)
#gDraw(parRs[0], parRs[1], colors, "wikiVote_500L_Blocked")

#parRs = BlockPartitioning.blockPartition("./network200.dat", 5, 30, 0.2, 4, 0.8, 1.2)
#gDraw(parRs[0], parRs[1], colors, "network200_Blocked")



