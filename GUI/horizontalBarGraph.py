import logging
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from GUI.commonPlotFunctions import CommonFunctions

import matplotlib as mpl
import matplotlib.pyplot as plt

import os
import numpy as np
import random
dirname = os.path.dirname(__file__)

logging.basicConfig(filename="../../log.log", level=logging.ERROR)
#https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py
class HorizontalGraph(FigureCanvas):
    def __init__(self, parent=None, width=7, height=5, dpi=100, updateCheck=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.alarmsPerHost = defaultdict(lambda: defaultdict(int))
        self.totalAlarmsPerSeverity = defaultdict(lambda: [])
        self.percentage=defaultdict(int)# TODO CLEAR IT WHEN UPDATE IS DONE
        self.setParent(parent)
        self.updateCheck = updateCheck
        #self.plotCode(self.axes)
        self.axes.invert_yaxis()
        self.axes.xaxis.set_visible(False)
        #self.axes.set_xlim(0,38)
        self.axes.set_title("Percentage of the various alarms ")


    def plotHOrizontalGraph(self,ax):
        getData = CommonFunctions()
        descriptionList,totalFractions = [],[]

        totAlarms=getData.countAlarms(self.totalAlarmsPerSeverity)


        for key, item in sorted(self.totalAlarmsPerSeverity.items()):
            descriptionList.append(getData.getInfo(key))
            totFraction=item/totAlarms
            totalFractions.append(totFraction*100)


        self.percentage['Cumulative Alarms'] = totalFractions

        for host in sorted(self.alarmsPerHost):
            singleFractions = []
            totPerHostAlarms=getData.countAlarms(self.alarmsPerHost[host])
            #print(totPerHostAlarms,"  ", self.alarmsPerHost[host])
            for ele in sorted(self.alarmsPerHost[host]):
                #print(self.alarmsPerHost[host][ele])
                singleFractions.append((self.alarmsPerHost[host][ele]/totPerHostAlarms)*100)
            self.percentage[host] = singleFractions


        #for host in self.alarmsPerHost:
        #self.singlePercentages[host]=


        labels = list(self.percentage.keys())

        data = np.array(list(self.percentage.values()))
        data_cum = data.cumsum(axis=1)

        colors_list = ['yellowgreen','orange','dodgerblue','red','rebeccapurple','black']
        try:
            colors = colors_list[0:len(totalFractions)]
        except IndexError:
            self.logger.info("Cannot plot. If you want to plot, you have to define more colors in the colors_list")


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
                ax.text(x, y, showPercentage, ha='center', va='center')#color=text_color)

        ax.legend(ncol=len(descriptionList), bbox_to_anchor=(0, -0.1),
                  loc='lower left', fontsize='small')

    def reStartPlot3(self):
        self.alarmsPerHost.clear()
        self.totalAlarmsPerSeverity.clear()
        self.percentage.clear()
        self.axes.invert_yaxis()
        self.axes.xaxis.set_visible(False)
        self.axes.set_title("Percentage of the various alarms ")

        getNewData = CommonFunctions()
        results = getNewData.fetchDataFromDB()
        self.alarmsPerHost = getNewData.organizeAlarmsPerHost(results)
        self.totalAlarmsPerSeverity = getNewData.organizeTotalAlarmsPerSeverity(results)

        self.plotHOrizontalGraph(self.axes)