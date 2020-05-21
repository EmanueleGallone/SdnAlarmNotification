"""
Author Fabio Carminati , 05-2020

This class defines the third graph: for each host (for all the hosts) we analyze the received alarms: we split them according to their severity
such that we can show their relative percentages w.r.t. the total alarms received from that host (from all the hosts).

The graph is updated every time the user clicks the RefreshButton on the GUI
(i.e. we redo the plot with the new data retrieved from the local DB)

Documentation of matplotlib has been found on: https://matplotlib.org/3.1.1/index.html
"""
from collections import defaultdict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from GUI.commonPlotFunctions import CommonFunctions
import datetime
import os
import numpy as np
import logging
dirname = os.path.dirname(__file__)

logging.basicConfig(filename="../log.log", level=logging.ERROR)

class Graph3(FigureCanvas):
    def __init__(self, parent=None, width=10, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.fig.patch.set_visible(False)
        FigureCanvas.__init__(self, self.fig)
        # self.alarmsPerHost: stores IPAddresses of the hosts and the correspondents severity alarms counters
        self.alarmsPerHost = defaultdict(lambda: defaultdict(int))
        # self.totalAlarmsPerSeverity: keys are the severities while the items are correspondent counters
        self.totalAlarmsPerSeverity = defaultdict(lambda: [])
        # self.percentage: keys are the host IpAddresses or a key='Overall alarms' for the cumulative scenario, while items
        # are the various percentages of the severity levels
        self.percentage=defaultdict(int)
        self.setParent(parent)
        self.axes.invert_yaxis()
        self.axes.xaxis.set_visible(False)
        self.axes.set_title("Percentage of the various alarms ",color='white')
        self.axes.text(0.5, 0.5, "No data", horizontalalignment='center', verticalalignment='center', fontsize=20)

    #RefreshButton has been clicked:redo the graph
    def reFreshGraph3(self):
        self.alarmsPerHost.clear()
        self.totalAlarmsPerSeverity.clear()
        self.percentage.clear()

        getNewData = CommonFunctions()
        results = getNewData.fetchDataFromDB()
        try:
            if (len(results)==0):
                raise Exception("No plot of graph 3")
            self.alarmsPerHost = getNewData.organizeAlarmsPerHost(results)
            self.totalAlarmsPerSeverity = getNewData.organizeTotalAlarmsPerSeverity(results)
            self.plotGraph3(self.axes)
        except Exception as e:
            logging.log(logging.ERROR, "The alarm table is empty: " + str(e))
            self.axes.text(0.5, 0.5, "Error loading data", horizontalalignment='center', verticalalignment='center',
                           fontsize=20)

    def plotGraph3(self,ax):
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_title("Percentage of the various alarms ", color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        getData = CommonFunctions()
        descriptionList,totalFractions = [],[]
        totAlarms=self.countAlarms(self.totalAlarmsPerSeverity)

        for key, item in sorted(self.totalAlarmsPerSeverity.items()):
            descriptionList.append(getData.getInfo(key))
            totFraction=item/totAlarms
            totalFractions.append(totFraction*100)

        self.percentage['Overall Alarms'] = totalFractions

        for host in sorted(self.alarmsPerHost):
            singleFractions = []
            totPerHostAlarms=self.countAlarms(self.alarmsPerHost[host])
            for ele in sorted(self.alarmsPerHost[host]):
                singleFractions.append((self.alarmsPerHost[host][ele]/totPerHostAlarms)*100)
            self.percentage[host] = singleFractions

        labels = list(self.percentage.keys())
        data = np.array(list(self.percentage.values()))
        data_cum = data.cumsum(axis=1)
        colors_list = ['yellowgreen','orange','red','rebeccapurple','dodgerblue','brown']

        try:
            if (len(colors_list)<len(totalFractions)):
                raise Exception("If you want to plot, you have to define more colors in the colors_list")

            colors = colors_list[0:len(totalFractions)]
            ax.invert_yaxis()
            ax.xaxis.set_visible(False)
            ax.set_xlim(0, np.sum(data, axis=1).max())

            for i, (colname, color) in enumerate(zip(descriptionList, colors)):
                widths = data[:, i]
                starts = data_cum[:, i] - widths
                ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)
                xcenters = starts + widths / 2

                for y, (x, c) in enumerate(zip(xcenters, widths)):
                    cString=str(round(c,1))
                    if(round(c,1)<1):
                        showPercentage=""
                    else:
                        showPercentage=cString+"%"
                    ax.text(x, y, showPercentage, ha='center', va='center')

            ax.legend(ncol=len(descriptionList), bbox_to_anchor=(0, -0.1),
                      loc='lower left', fontsize='small')
            infoRefresh="Last reFresh at time:"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ax.text(0, -0.12, infoRefresh, verticalalignment='center',color='white',
                    transform=ax.transAxes)

        except Exception as e:
            logging.log(logging.ERROR, "Cannot plot: " +str(e))

    #The user has required to save either this graph or all the graphs
    def saveGraph3(self, directory):
        path = directory + "\graph3.png"
        saveObject = CommonFunctions()
        saveObject.saveSingleGraph(path, self.fig,3)

    def countAlarms(self,dict):
        totAlarms=0
        for key, item in sorted(dict.items()):
            totAlarms = totAlarms + item
        return totAlarms
