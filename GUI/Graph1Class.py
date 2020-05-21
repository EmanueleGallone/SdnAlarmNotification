"""
Author Fabio Carminati , 05-2020

This class defines the first graph: on the x-axis there are all the various severity levels (fetched from the config.json file )
while on the y-axis there are the correspondent number of alarms received from each host (fetched from the local DB)

The graph is updated every time the user clicks the RefreshButton on the GUI
(i.e. we redo the plot with the new data retrieved from the local DB)

Documentation of matplotlib has been found on: https://matplotlib.org/3.1.1/index.html
"""
from GUI.commonPlotFunctions import CommonFunctions
from collections import defaultdict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import numpy as np
import datetime
import logging
dirname = os.path.dirname(__file__)

logging.basicConfig(filename="../log.log", level=logging.ERROR)

class Graph1(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5.3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_visible(False)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        # self.alarmsPerHost: stores IPAddresses of the hosts and the correspondents severity alarms counters
        self.alarmsPerHost = defaultdict(lambda: defaultdict(int))
        # self.totalAlarmsPerSeverity: keys are the severities while the items are correspondent counters
        self.totalAlarmsPerSeverity = defaultdict(int)
        self.setParent(parent)
        self.axes.set_xlabel("Severity Level",color='white')
        self.axes.set_ylabel("Number of alarms",color='white')
        self.axes.set_title("Alarms received per host ",color='white')
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.text(0.5, 0.5,"No data",horizontalalignment='center',verticalalignment='center',fontsize=20)

    #RefreshButton has been clicked
    def reFreshGraph1(self):
        self.alarmsPerHost.clear()
        self.totalAlarmsPerSeverity.clear()

        getData = CommonFunctions()
        results = getData.fetchDataFromDB()

        try:
            if (len(results)==0):
                raise Exception("No plot of graph 1")
            self.alarmsPerHost = getData.organizeAlarmsPerHost(results)
            self.totalAlarmsPerSeverity = getData.organizeTotalAlarmsPerSeverity(results)
            self.plotGraph1(self.axes)
        except Exception as e:
            logging.log(logging.ERROR, "The alarm table is empty: " + str(e))
            self.axes.text(0.5, 0.5, "Error loading data", horizontalalignment='center', verticalalignment='center', fontsize=20)

    def plotGraph1(self, ax):
        ax.set_xlabel("Severity Level",color='white')
        ax.set_ylabel("Number of alarms",color='white')
        ax.set_title("Alarms received per host ",color='white')

        reverseDictionary=defaultdict(lambda: defaultdict(int))
        ipList=[]
        for host in sorted(self.alarmsPerHost):
            for severity in sorted(self.alarmsPerHost[host]):
                reverseDictionary[severity][host]=self.alarmsPerHost[host][severity]
            ipList.append(host)

        rects,descriptionList=[],[]
        getDescription=CommonFunctions()
        for severity in sorted(reverseDictionary):
            descriptionList.append(getDescription.getInfo(int(severity)))

        for ip in sorted(ipList):
            means = []
            for severity in sorted(reverseDictionary):
                means.append(reverseDictionary[severity][ip])
            rects.append(means)

        x = np.arange(len(self.totalAlarmsPerSeverity))
        width = 1.5 / len(reverseDictionary)

        for i in range(0, len(rects)):
            bar=ax.bar(x + (i - (len(rects) - 1) / 2) * width / 2, rects[i],width / 2,label=list(ipList)[i])
            getDescription.autolabel(bar,ax)

        ax.set_xticks(x)
        ax.set_xticklabels(descriptionList)

        yAverageList = []
        xAverageList = []
        for key, item in sorted(self.totalAlarmsPerSeverity.items()):
            avg = item / len(self.alarmsPerHost)
            yAverageList.append(avg)
            xAverageList.append(int(key))

        ax.plot(xAverageList, yAverageList, color='red', linestyle='--',marker='o', label="Average number of alarms per severity")
        ax.legend(fancybox=True, framealpha=0.2)
        infoRefresh = "Last reFresh at time:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ax.text(0, -0.12, infoRefresh, verticalalignment='center',
                transform=ax.transAxes,color='white')

    #The user has required to save either this graph or all the graphs
    def saveGraph1(self, directory):
        path=directory+"\graph1.png"
        saveObject=CommonFunctions()
        saveObject.saveSingleGraph(path,self.fig,1)


