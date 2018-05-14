#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
a test for chart drawing

"""
import plotly
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
import plotly.graph_objs as go

from plotly import tools

import RandomWalkToy
import BlockPartitioning
import RandomPartitioning
import GetRWTrack

def RWTdraw(ydatas, numOfPars, lengthOfRW, namesOfPars):
    # notice: the len(ydatas) should be equal to len(namesOfPars)
    numGraphs = len(ydatas)
    if numGraphs < 1:
        return None
    #print "num of Graphs: ",numGraphs
    subTi = []
    for i in range(0, numGraphs):
        subTi.append(namesOfPars[i]+' Partitioning')
    subTitles = tuple(subTi)

    fig = tools.make_subplots(rows=((numGraphs+1)/2), cols=2, subplot_titles=subTitles)


    for i in range(0, numGraphs):
        xa = ya = str(i+1)

        x_data = []
        for t in range(0, numOfPars):
            x_data.append([])
        for z in range(0, numOfPars):
            for j in range(1, lengthOfRW+1):
                x_data[z].append(j)
        #print "i: ", i
        #print "ydatas[i]: ", ydatas[i]
        y_data = ydatas[i]

        trace = []
        namePar = namesOfPars[i]

        for l in range(0, numOfPars):
            trace.append(go.Scatter(
                x=x_data[l],
                y=y_data[l],
                mode='lines',
                hoverinfo='none',
                #name = 'Track of RW in '+namePar,
                line=dict(width=6, color='rgb(104, 104, 204)'),
                #line=dict(width=line_size[l]),
                connectgaps=False,
            ))
        for tra in trace:
            fig.append_trace(tra, i/2 + 1, i%2 + 1)
        # All of the axes properties here: https://plot.ly/python/reference/#XAxis
        fig['layout']['xaxis'+xa].update(title='Step # in Random Walk', showgrid=False)
        # All of the axes properties here: https://plot.ly/python/reference/#YAxis
        fig['layout']['yaxis'+ya].update(title='Partition #', showgrid=False)

    fig['layout'].update(title='======= The Track of Random Walk ======>', showlegend=False)

    pu = plotly.offline.plot(fig, auto_open=False, filename="RWTrack_Graphs.html")

    print "pu: ", pu

    return pu



'''
visT = RandomWalkToy.randomWalk("./network200.dat", 200)
parRs1 = BlockPartitioning.blockPartition("./network200.dat", 5, 30, 0.2, 4, 0.8, 1.2)
pt1 = GetRWTrack.getTrackDetail(visT[2], parRs1[0],5)

parRs2 = RandomPartitioning.RVC("./network200.dat", 5)
pt2 = GetRWTrack.getTrackDetail(visT[2], parRs2[0], 5)

parRs3 = RandomPartitioning.EP2D("./network200.dat", 5)
pt3 = GetRWTrack.getTrackDetail(visT[2], parRs3[0], 5)

RWTdraw([pt1,pt2,pt3], 5, 200, ['Blocked', 'RVC', 'EP2D'])

'''









'''

numOfPars = 4
partitioningName = "***"+" Partitions"

title = 'The Track of Random Walk over '+partitioningName

labels = []
for i in range(1, numOfPars+1):
    labels.append("Partition "+str(i))
#labels = ['Partition 1', 'Partition 2', 'Partition 3', 'Partition 4']

colors = []
for i in range(0, numOfPars):
    colors.append("rgb("+str(105+i*35)+","+str(52+i*5)+","+str(24+i*15)+")")

#colors = ['rgba(67,67,67,1)', 'rgba(115,115,115,1)', 'rgba(49,130,189, 1)', 'rgba(189,189,189,1)']

mode_size = []
for i in range(0, numOfPars):
    mode_size.append(8)
#mode_size = [8, 8, 8, 8]

line_size = []
for i in range(0, numOfPars):
    line_size.append(6)
#line_size = [3, 3, 3, 3]


x_data = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
]

y_data = [
    ["Partition 1", "Partition 1", "Partition 1", "Partition 1", None, None, None, None, None, None, "Partition 1", "Partition 1", "Partition 1", "Partition 1", "Partition 1"],
    [None, None, None, "Partition 2", "Partition 2", "Partition 2", "Partition 2", "Partition 2", "Partition 2", None, None, None, None, None, None],
    [None, None, None, None, None, None, None, "Partition 3", "Partition 3", "Partition 3", "Partition 3", None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, "Partition 4", "Partition 4", "Partition 4"],
]

traces = []

for i in range(0, numOfPars):

    traces.append(go.Scatter(
        x=x_data[i],
        y=y_data[i],
        mode='lines',
        hoverinfo='none',
        line=dict(color=colors[i], width=line_size[i]),
        #line=dict(width=line_size[i]),
        connectgaps=False,
    ))



layout = go.Layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        autotick=False,
        ticks='outside',
        tickcolor='rgb(204, 204, 204)',
        tickwidth=2,
        ticklen=5,
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=False,
)

annotations = []

# Adding labels
for y_trace, label, color in zip(y_data, labels, colors):
    # labeling the left_side of the plot
    t = 0
    for i in range(0, len(y_trace)):
        if t==0 and y_trace[i]:
            t = i

    annotations.append(dict(xref='paper', x=-0.02, y=y_trace[t],
                                  xanchor='right', yanchor='middle',
                                  text=label,
                                  font=dict(family='Arial',
                                            size=16,
                                            color=colors,),
                                  showarrow=False))


# Title
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.05,
                              xanchor='center', yanchor='bottom',
                              text=title,
                              font=dict(family='Arial',
                                        size=20,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                        xanchor='center', yanchor='top',
                        text='Step # in Random Walk',
                        font=dict(family='Arial',
                                  size=12,
                                  color='rgb(150,150,150)'),
                        showarrow=False))

#layout['annotations'] = annotations

#fig = go.Figure(data=traces, layout=layout)
fig = go.Figure(data=traces)


pu = plotly.offline.plot(fig, auto_open=False, filename="LineChartTest.html")

print "pu: ", pu

'''