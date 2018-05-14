#!/usr/bin/python
# -*- coding: utf-8 -*-

# the main program to create UI of Graph Partitioning Demostration

import os
import wx
import BlockPartitioning
import RandomPartitioning
import PowerGraphPartitioning
import GraphDraw_plotly
import GraphDraw_plotly_RW
import RandomWalkToy
import plotly
import wx.html2
import webbrowser
import GetRWTrack
import RWTrack_plot


wildcard = "Python source (*.py)|*.py|" \
           "All files (*.*)|*.*"


class Demo(wx.Frame):
    dsFilePa = "/Users/yifanli/Data/data_test.txt"
    # the checked partition methods
    checkedParMethods = []
    block_html_loc = ""
    rvc_html_loc = ""
    crv_html_loc = ""
    ep1D_html_loc = ""
    ep2D_html_loc = ""
    pg_html_loc = ""

    # the page of showing tracks of random walks
    track_html_loc = ""

    def __init__(self, parent, title):
        super(Demo, self).__init__(parent, title=title,
                                   size=(1020, 820))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        # dsF = self.dsFilePa

        self.panel = wx.Panel(self)
        self.currentDirectory = os.getcwd()
        self.parbgcol = "LIGHT STEEL BLUE"
        self.changedcol = "CADET BLUE"

        #block_html_loc = ""

        sizer = wx.GridBagSizer(5, 5)

        text1 = wx.StaticText(self.panel, label="BlockedPartitioning v.s. Others")
        sizer.Add(text1, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=15)

        icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap('SN.png'))
        sizer.Add(icon, pos=(0, 3), flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT,
                  border=5)

        line = wx.StaticLine(self.panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)

        # ----------------------
        text2 = wx.StaticText(self.panel, label="Graph Dataset:")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT | wx.TOP, border=10)

        #tc2 = wx.TextCtrl(self.panel)
        self.panel.tc2 = wx.StaticText(self.panel, label="")
        sizer.Add(self.panel.tc2, pos=(2, 1), span=(1, 2.8), flag=wx.TOP|wx.EXPAND, border=5)

        button1 = wx.Button(self.panel, label="Browse...")
        button1.Bind(wx.EVT_BUTTON, self.onOpenFile)
        sizer.Add(button1, pos=(2, 3), flag=wx.TOP | wx.RIGHT, border=5)

        # ----------------------
        text3 = wx.StaticText(self.panel, label="PartitioningMethod:")
        sizer.Add(text3, pos=(3, 0), flag=wx.TOP | wx.LEFT, border=10)

        parMethods = ['1# Blocked Partitioning', '2# RandomVertexCut',
                      '3# CanonicalRandomVertexCut', '4# EdgePartition1D', '5# EdgePartition2D', '6# PowerGraph']
        '''
        combo1 = wx.ComboBox(self.panel, choices=parMethods)
        sizer.Add(combo1, pos=(3, 1), span=(1, 3),
            flag=wx.TOP|wx.EXPAND, border=5)
        '''
        # the checkButton of ALL partitionings
        # allCheckedBu = wx.CheckBox(panel, label = "All Partition Methods", style = wx.CHK_3STATE)
        # sizer.Add(allCheckedBu, pos=(3, 1), span = (1,2), flag=wx.TOP|wx.EXPAND, border=5)

        # the CheckListBox of ALL partitionings
        self.panel.citList = wx.CheckListBox(self.panel, choices=parMethods)
        sizer.Add(self.panel.citList, pos=(3, 1), span=(1, 1.5), flag=wx.TOP | wx.EXPAND, border=5)
        self.panel.citList.Bind(wx.EVT_CHECKLISTBOX, self.onCheckedListBox)

        # button2 = wx.Button(self.panel, label="Browse...")
        # sizer.Add(button2, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)

        # --------------------
        text4 = wx.StaticText(self.panel, label="Number of Partitions:")
        sizer.Add(text4, pos=(4, 0), flag=wx.LEFT, border=10)

        self.panel.tc3 = wx.TextCtrl(self.panel)
        sizer.Add(self.panel.tc3, pos=(4, 1), span=(1, 1.5), flag=wx.TOP | wx.EXPAND)

        # --------------------
        sb1 = wx.StaticBox(self.panel, label="Optional Parameters")

        #boxsizer1 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
        boxsizer1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(self.panel, label="Max Radius of Closeness Computation(>3):              "))
        self.panel.tc_ld = wx.TextCtrl(self.panel)
        hbox1.Add(self.panel.tc_ld, flag=wx.LEFT, border=5)
        boxsizer1.Add(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(self.panel, label="Decay Factor in Closeness Computation(0.0 ~ 1.0):  "))
        self.panel.tc_df = wx.TextCtrl(self.panel)
        hbox2.Add(self.panel.tc_df, flag=wx.LEFT, border=5)
        boxsizer1.Add(hbox2)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(wx.StaticText(self.panel, label="Upper Bound of Balancing(1.0 - 2.0):                        "))
        self.panel.tc_ub = wx.TextCtrl(self.panel)
        hbox3.Add(self.panel.tc_ub, flag=wx.LEFT, border=5)
        boxsizer1.Add(hbox3)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(wx.StaticText(self.panel, label="Lower Bound of Balancing(0.0 - 1.0):                        "))
        self.panel.tc_lb = wx.TextCtrl(self.panel)
        hbox4.Add(self.panel.tc_lb, flag=wx.LEFT, border=5)
        boxsizer1.Add(hbox4)

        # boxsizer1.Add(wx.CheckBox(panel, label="A"), flag=wx.LEFT|wx.TOP, border=5)

        sizer.Add(boxsizer1, pos=(3, 2),flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        #sizer.Add(boxsizer1, pos=(5, 0), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        # ---------------------

        button3 = wx.Button(self.panel, label='Help')
        sizer.Add(button3, pos=(5, 0), flag=wx.LEFT, border=10)

        button4 = wx.Button(self.panel, label="Run")
        button4.Bind(wx.EVT_BUTTON, self.onRun)
        sizer.Add(button4, pos=(5, 3))

        #button5 = wx.Button(self.panel, label="Cancel")
        #sizer.Add(button5, pos=(5, 4), span=(1, 1), flag=wx.BOTTOM | wx.RIGHT, border=5)

        # --------------------
        line2 = wx.StaticLine(self.panel)
        sizer.Add(line2, pos=(6, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)
        # --------------------
        sb2 = wx.StaticBox(self.panel, label="Results of Selected Partitioning(s), e.g. VRF...")

        #txt =''' Vertices: 35,\n Edges: 109, \n VRF: 2.35'''
        txt = "... \n..."
        boxsizerPR = wx.StaticBoxSizer(sb2, wx.HORIZONTAL)

        #partitoning result #1
        bs1 = wx.BoxSizer(wx.VERTICAL)
        t1 = wx.StaticText(self.panel, label="Partitioning #1:")
        #self.panel.bst1 = wx.StaticText(self.panel, label=txt)
        self.panel.bst1 = wx.TextCtrl(self.panel, -1, txt, size=(160,170),
                              style=wx.TE_MULTILINE | wx.ALIGN_LEFT | wx.DOUBLE_BORDER)
        self.panel.bst1.SetBackgroundColour(self.parbgcol)
        self.panel.bssbut1 = wx.Button(self.panel, label='Show in WebBrowser')
        #self.panel.savebut1 = wx.Button(self.panel, label='Save Partitions')
        bs1.Add(t1, flag=wx.LEFT | wx.TOP)
        bs1.Add(self.panel.bst1, border=5)
        bs1.Add(self.panel.bssbut1)
        #bs1.Add(self.panel.savebut1)
        self.panel.bst1.Bind(wx.EVT_SET_FOCUS, self.onClickChangeCol)
        self.panel.bssbut1.Bind(wx.EVT_BUTTON, self.onClickOpenWebBro01)
        #print "self.block_html_loc: ",self.block_html_loc
        #self.panel.bssbut1.Bind(wx.EVT_BUTTON, self.getClickOpenWebBro(self))

        # partitoning result #2
        bs2 = wx.BoxSizer(wx.VERTICAL)
        t2 = wx.StaticText(self.panel, label="Partitioning #2:")
        #self.panel.bst2 = wx.StaticText(self.panel, label=txt)
        self.panel.bst2 = wx.TextCtrl(self.panel, -1, txt, size=(160,170),
                              style=wx.TE_MULTILINE | wx.ALIGN_LEFT | wx.DOUBLE_BORDER)
        self.panel.bst2.SetBackgroundColour(self.parbgcol)
        self.panel.bssbut2 = wx.Button(self.panel, label='Show in WebBrowser')
        #self.panel.savebut2 = wx.Button(self.panel, label='Save Partitions')
        bs2.Add(t2, flag=wx.LEFT | wx.TOP)
        bs2.Add(self.panel.bst2, border=5)
        bs2.Add(self.panel.bssbut2)
        #bs2.Add(self.panel.savebut2)
        self.panel.bst2.Bind(wx.EVT_SET_FOCUS, self.onClickChangeCol)
        self.panel.bssbut2.Bind(wx.EVT_BUTTON, self.onClickOpenWebBro02)

        # partitoning result #3
        bs3 = wx.BoxSizer(wx.VERTICAL)
        t3 = wx.StaticText(self.panel, label="Partitioning #3:")
        self.panel.bst3 = wx.TextCtrl(self.panel, -1, txt, size=(160,170),
                              style=wx.TE_MULTILINE | wx.ALIGN_LEFT | wx.DOUBLE_BORDER)
        self.panel.bst3.SetBackgroundColour(self.parbgcol)
        self.panel.bssbut3 = wx.Button(self.panel, label='Show in WebBrowser')
        #self.panel.savebut3 = wx.Button(self.panel, label='Save Partitions')
        bs3.Add(t3, flag=wx.LEFT | wx.TOP)
        bs3.Add(self.panel.bst3, border=5)
        bs3.Add(self.panel.bssbut3)
        #bs3.Add(self.panel.savebut3)
        self.panel.bst3.Bind(wx.EVT_SET_FOCUS, self.onClickChangeCol)
        self.panel.bssbut3.Bind(wx.EVT_BUTTON, self.onClickOpenWebBro03)

        # partitoning result #4
        bs4 = wx.BoxSizer(wx.VERTICAL)
        t4 = wx.StaticText(self.panel, label="Partitioning #4:")
        self.panel.bst4 = wx.TextCtrl(self.panel, -1, txt, size=(160,170),
                              style=wx.TE_MULTILINE | wx.ALIGN_LEFT | wx.DOUBLE_BORDER)
        self.panel.bst4.SetBackgroundColour(self.parbgcol)
        self.panel.bssbut4 = wx.Button(self.panel, label='Show in WebBrowser')
        #self.panel.savebut4 = wx.Button(self.panel, label='Save Partitions')
        bs4.Add(t4, flag=wx.LEFT | wx.TOP)
        bs4.Add(self.panel.bst4, border=5)
        bs4.Add(self.panel.bssbut4)
        #bs4.Add(self.panel.savebut4)
        self.panel.bst4.Bind(wx.EVT_SET_FOCUS, self.onClickChangeCol)
        self.panel.bssbut4.Bind(wx.EVT_BUTTON, self.onClickOpenWebBro04)

        # partitoning result #5
        bs5 = wx.BoxSizer(wx.VERTICAL)
        t5 = wx.StaticText(self.panel, label="Partitioning #5:")
        self.panel.bst5 = wx.TextCtrl(self.panel, -1, txt, size=(160,170),
                              style=wx.TE_MULTILINE | wx.ALIGN_LEFT | wx.DOUBLE_BORDER)
        self.panel.bst5.SetBackgroundColour(self.parbgcol)
        self.panel.bssbut5 = wx.Button(self.panel, label='Show in WebBrowser')
        #self.panel.savebut5 = wx.Button(self.panel, label='Save Partitions')
        bs5.Add(t5, flag=wx.LEFT | wx.TOP)
        bs5.Add(self.panel.bst5, border=5)
        bs5.Add(self.panel.bssbut5)
        #bs5.Add(self.panel.savebut5)
        self.panel.bst5.Bind(wx.EVT_SET_FOCUS, self.onClickChangeCol)
        self.panel.bssbut5.Bind(wx.EVT_BUTTON, self.onClickOpenWebBro05)

        # partitoning result #6
        bs6 = wx.BoxSizer(wx.VERTICAL)
        t6 = wx.StaticText(self.panel, label="Partitioning #6:")
        self.panel.bst6 = wx.TextCtrl(self.panel, -1, txt, size=(160,170),
                              style=wx.TE_MULTILINE | wx.ALIGN_LEFT | wx.DOUBLE_BORDER)
        self.panel.bst6.SetBackgroundColour(self.parbgcol)
        self.panel.bssbut6 = wx.Button(self.panel, label='Show in WebBrowser')
        #self.panel.savebut6 = wx.Button(self.panel, label='Save Partitions')
        bs6.Add(t6, flag=wx.LEFT | wx.TOP)
        bs6.Add(self.panel.bst6, border=5)
        bs6.Add(self.panel.bssbut6)
        #bs6.Add(self.panel.savebut6)
        self.panel.bst6.Bind(wx.EVT_SET_FOCUS, self.onClickChangeCol)
        self.panel.bssbut6.Bind(wx.EVT_BUTTON, self.onClickOpenWebBro06)

        boxsizerPR.Add(bs1)
        boxsizerPR.AddSpacer(5)
        boxsizerPR.Add(bs2)
        boxsizerPR.AddSpacer(5)
        boxsizerPR.Add(bs3)
        boxsizerPR.AddSpacer(5)
        boxsizerPR.Add(bs4)
        boxsizerPR.AddSpacer(5)
        boxsizerPR.Add(bs5)
        boxsizerPR.AddSpacer(5)
        boxsizerPR.Add(bs6)

        # boxsizer2.Add(wx.StaticText(self.panel, label=txt), flag=wx.ALL, border=5)


        sizer.Add(boxsizerPR, pos=(7, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # --------------------
        line3 = wx.StaticLine(self.panel)
        sizer.Add(line3, pos=(8, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)
        # --------------------

        # the toy of random walk
        # 1) select a starting vertex (randomly?)
        # 2) launch a random walk from above vertex of length L, L is pre-set
        sb3 = wx.StaticBox(self.panel, label="Toy: launch a random walk from a random vertex...")
        boxsizerRW = wx.StaticBoxSizer(sb3, wx.HORIZONTAL)

        lenRW = wx.StaticText(self.panel, label="Length of Random Walk: ")
        self.panel.tc_lrw = wx.TextCtrl(self.panel)
        buttonLa = wx.Button(self.panel, label="Launch")
        buttonLa.Bind(wx.EVT_BUTTON, self.onLaunch)

        #buttonShowRW = wx.Button(self.panel, label="The results are displayed in above <Show in WebBrowser>")
        states = wx.StaticText(self.panel, label=": click the <Show in WebBrowser> above to see results...")

        #button4.Bind(wx.EVT_BUTTON, self.onShowRW)

        boxsizerRW.Add(lenRW, 0, wx.ALL|wx.LEFT, 5)
        boxsizerRW.Add(self.panel.tc_lrw, 0, wx.ALL|wx.LEFT, 5)
        boxsizerRW.Add(buttonLa, 0, wx.ALL|wx.LEFT, 5)
        boxsizerRW.Add(states, 0, wx.ALL|wx.LEFT, 5)

        sizer.Add(boxsizerRW, pos=(9, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # to browse the tracks of random walks in different partitioning
        sb4 = wx.StaticBox(self.panel, label="To browse the track of random walks in different partitions:")
        boxsizerTra = wx.StaticBoxSizer(sb4, wx.HORIZONTAL)

        buttonTra = wx.Button(self.panel, label="Browse")
        buttonTra.Bind(wx.EVT_BUTTON, self.onTrack)

        boxsizerTra.Add(buttonTra, 0, wx.ALL|wx.LEFT, 5)
        sizer.Add(boxsizerTra, pos=(10, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)







        '''
        # the box to display html
        html_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.browser = wx.html2.WebView.New(self.panel, size=(400,250))
        html_sizer.Add(self.panel.browser)

        sizer.Add(html_sizer, pos=(8, 0), span=(1,5),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        '''
        #sizer.AddGrowableCol(2)

        self.panel.SetSizer(sizer)

    def onLaunch(self, event):
        # the length of Random Walk in toy
        lengthOfRW = int(self.panel.tc_lrw.GetValue())

        edgeListFile = self.panel.tc2.Label
        numOfPar = int(self.panel.tc3.GetValue())
        numOfBlo = 10 * numOfPar
        tel = float(self.panel.tc_df.GetValue())
        depOfBFS = int(self.panel.tc_ld.GetValue())
        lowerBound = float(self.panel.tc_lb.GetValue())
        upperBound = float(self.panel.tc_ub.GetValue())

        visT = RandomWalkToy.randomWalk(edgeListFile, lengthOfRW)

        # the y_data of random walk's track
        RWTracks = []
        # the names of selected partitions
        namesOfPars = []

        for checked in self.checkedParMethods:
            # blocked partitioning
            if checked == 0:
                res = BlockPartitioning.blockPartition(edgeListFile, numOfPar, numOfBlo, tel, depOfBFS, lowerBound,
                                                       upperBound)
                self.block_html_loc = GraphDraw_plotly_RW.gDraw(res[0], res[1], GraphDraw_plotly.colors, "blocked",
                                                                visT[0], visT[1], lengthOfRW)
                txt = res[2] + "\n" + "The Random Walk Toy is done!"
                self.panel.bst1.SetValue(txt)

                pt = GetRWTrack.getTrackDetail(visT[2], res[0], numOfPar)
                RWTracks.append(pt)
                namesOfPars.append('Blocked')

                self.panel.Layout()

            # random vertex cut
            if checked == 1:
                res = RandomPartitioning.RVC(edgeListFile, numOfPar)
                self.rvc_html_loc = GraphDraw_plotly_RW.gDraw(res[0], res[1], GraphDraw_plotly.colors, "RVC",
                                                              visT[0], visT[1], lengthOfRW)
                txt = res[2] + "\n" + "The Random Walk Toy is done!"
                self.panel.bst2.SetValue(txt)

                pt = GetRWTrack.getTrackDetail(visT[2], res[0], numOfPar)
                RWTracks.append(pt)
                namesOfPars.append('RandomVertexCut(RVC)')

                self.panel.Layout()

            # canonical random vertex cut
            if checked == 2:
                res = RandomPartitioning.CRV(edgeListFile, numOfPar)
                self.crv_html_loc = GraphDraw_plotly_RW.gDraw(res[0], res[1], GraphDraw_plotly.colors, "CRV",
                                                              visT[0], visT[1], lengthOfRW)
                txt = res[2] + "\n" + "The Random Walk Toy is done!"
                self.panel.bst3.SetValue(txt)

                pt = GetRWTrack.getTrackDetail(visT[2], res[0], numOfPar)
                RWTracks.append(pt)
                namesOfPars.append('CanonicalRandomVertexCut(CRVC)')

                self.panel.Layout()

            # EdgePartition1D
            if checked == 3:
                res = RandomPartitioning.EP1D(edgeListFile, numOfPar)
                self.ep1D_html_loc = GraphDraw_plotly_RW.gDraw(res[0], res[1], GraphDraw_plotly.colors, "EP1D",
                                                               visT[0], visT[1], lengthOfRW)
                txt = res[2] + "\n" + "The Random Walk Toy is done!"
                self.panel.bst4.SetValue(txt)

                pt = GetRWTrack.getTrackDetail(visT[2], res[0], numOfPar)
                RWTracks.append(pt)
                namesOfPars.append('EdgePartition1D(EP1D)')

                self.panel.Layout()

            # EdgePartition2D
            if checked == 4:
                res = RandomPartitioning.EP2D(edgeListFile, numOfPar)
                self.ep2D_html_loc = GraphDraw_plotly_RW.gDraw(res[0], res[1], GraphDraw_plotly.colors, "EP2D",
                                                               visT[0], visT[1], lengthOfRW)
                txt = res[2] + "\n" + "The Random Walk Toy is done!"
                self.panel.bst5.SetValue(txt)

                pt = GetRWTrack.getTrackDetail(visT[2], res[0], numOfPar)
                RWTracks.append(pt)
                namesOfPars.append('EdgePartition2D(EP2D)')

                self.panel.Layout()

            # PowerGraph
            if checked == 5:
                res = PowerGraphPartitioning.PowerGraphPar(edgeListFile, numOfPar)
                self.pg_html_loc = GraphDraw_plotly_RW.gDraw(res[0], res[1], GraphDraw_plotly.colors, "PowerG",
                                                             visT[0], visT[1], lengthOfRW)
                txt = res[2] + "\n" + "The Random Walk Toy is done!"
                self.panel.bst6.SetValue(txt)

                pt = GetRWTrack.getTrackDetail(visT[2], res[0], numOfPar)
                RWTracks.append(pt)
                namesOfPars.append('PowerGraph')

                self.panel.Layout()

        self.track_html_loc = RWTrack_plot.RWTdraw(RWTracks, numOfPar, lengthOfRW, namesOfPars)
        print self.track_html_loc

    # the button to browse tracks of random walks
    def onTrack(self, event):
        print "opening tracks page..."
        webbrowser.open(self.track_html_loc)




    def onRun(self, event):
        # to make the partitioning(s)
        # test: blocked
        edgeListFile = self.panel.tc2.Label
        numOfPar = int(self.panel.tc3.GetValue())
        numOfBlo = 10 * numOfPar
        tel = float(self.panel.tc_df.GetValue())
        depOfBFS = int(self.panel.tc_ld.GetValue())
        lowerBound = float(self.panel.tc_lb.GetValue())
        upperBound = float(self.panel.tc_ub.GetValue())

        for checked in self.checkedParMethods:
            # blocked partitioning
            if checked == 0:
                res = BlockPartitioning.blockPartition(edgeListFile, numOfPar, numOfBlo, tel, depOfBFS, lowerBound, upperBound)
                # to draw the test graph
                #GraphDraw.gDraw(GraphDraw.edges, GraphDraw.nodes, GraphDraw.colors, "test01")
                self.block_html_loc = GraphDraw_plotly.gDraw(res[0], res[1], GraphDraw_plotly.colors, "blocked")
                #print "self:", self.block_html_loc
                self.panel.bst1.SetValue(res[2])
                self.panel.Layout()

            # random vertex cut
            if checked == 1:
                res = RandomPartitioning.RVC(edgeListFile, numOfPar)
                self.rvc_html_loc = GraphDraw_plotly.gDraw(res[0], res[1], GraphDraw_plotly.colors, "RVC")
                self.panel.bst2.SetValue(res[2])
                self.panel.Layout()

            # canonical random vertex cut
            if checked == 2:
                res = RandomPartitioning.CRV(edgeListFile, numOfPar)
                self.crv_html_loc = GraphDraw_plotly.gDraw(res[0], res[1], GraphDraw_plotly.colors, "CRV")
                self.panel.bst3.SetValue(res[2])
                self.panel.Layout()

            # EdgePartition1D
            if checked == 3:
                res = RandomPartitioning.EP1D(edgeListFile, numOfPar)
                self.ep1D_html_loc = GraphDraw_plotly.gDraw(res[0], res[1], GraphDraw_plotly.colors, "EP1D")
                self.panel.bst4.SetValue(res[2])
                self.panel.Layout()

            # EdgePartition2D
            if checked == 4:
                res = RandomPartitioning.EP2D(edgeListFile, numOfPar)
                self.ep2D_html_loc = GraphDraw_plotly.gDraw(res[0], res[1], GraphDraw_plotly.colors, "EP2D")
                self.panel.bst5.SetValue(res[2])
                self.panel.Layout()

            # PowerGraph
            if checked == 5:
                res = PowerGraphPartitioning.PowerGraphPar(edgeListFile, numOfPar)
                self.pg_html_loc = GraphDraw_plotly.gDraw(res[0], res[1], GraphDraw_plotly.colors, "PowerG")
                self.panel.bst6.SetValue(res[2])
                self.panel.Layout()





        # test: to display html
        #self.panel.browser.LoadURL("/Users/yifanli/PycharmProjects/demo_partition/wikiVote_plotly.html")
        #self.panel.Layout()
        #self.panel.Show()
        print "runing....done!"

    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            #for path in paths:
            #    print path
                #self.dsFilePa = path
        # print "self.dsFilePa:"
        # print self.dsFilePa
        self.panel.tc2.Label = paths[0]
        self.panel.Layout()
        dlg.Destroy()

    def onCheckedListBox(self, event):
        # the handler of CheckListBox of partitioning methods
        check = event.EventObject
        # checkedParMethods = []
        # checkedParMethods = [i for i in range(self.panel.citList.GetCount()) if self.panel.citList.IsChecked(i)]
        #self.checkedParMethods = check.GetCheckedStrings()
        self.checkedParMethods = check.GetChecked()
        print self.checkedParMethods

    def onClickChangeCol(self, event):
        print "click!!!"
        obj = event.EventObject
        obj.SetBackgroundColour(self.changedcol)
        #event.Skip()
        #event.ResumePropagation(1)

    # display blocked partitioning graph in Web Browser
    def onClickOpenWebBro01(self, event):
        print "open web browser..."
        #webbrowser.get(safari_path).open("file://" + "/Users/yifanli/PycharmProjects/demo_partition/t_plotly.html")
        webbrowser.open(self.block_html_loc)

    def onClickOpenWebBro02(self, event):
        print "open web browser..."
        webbrowser.open(self.rvc_html_loc)

    def onClickOpenWebBro03(self, event):
        print "open web browser..."
        webbrowser.open(self.crv_html_loc)

    def onClickOpenWebBro04(self, event):
        print "open web browser..."
        webbrowser.open(self.ep1D_html_loc)

    def onClickOpenWebBro05(self, event):
        print "open web browser..."
        webbrowser.open(self.ep2D_html_loc)

    def onClickOpenWebBro06(self, event):
        print "open web browser..."
        webbrowser.open(self.pg_html_loc)




if __name__ == '__main__':
    app = wx.App()
    Demo(None, title="SGVCut(Social Graph Partitioning Tool)")
    app.MainLoop()