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
        self.percentage=defaultdict(int)

        #self.axes.margins(0)
        self.plotHOrizontalGraph(self.axes)
    def plotHOrizontalGraph(self,ax):
        getData = CommonFunctions()
        results = getData.fetchDataFromDB()
        self.alarmsPerHost = getData.organizeAlarmsPerHost(results)
        self.totalAlarmsPerSeverity = getData.organizeTotalAlarmsPerSeverity(results)

        descriptionList = []
        totAlarms=0
        for key, item in sorted(self.totalAlarmsPerSeverity.items()):
            getData = CommonFunctions()
            descriptionList.append(getData.getInfo(key))
            totAlarms=totAlarms+item

        fractions=[]
        for key, item in sorted(self.totalAlarmsPerSeverity.items()):
            fraction=item/totAlarms
            fractions.append(fraction*100)

        self.percentage['Cumulative Error']=fractions
        self.percentage['h1']=fractions

        labels = list(self.percentage.keys())

        data = np.array(list(self.percentage.values()))
        data_cum = data.cumsum(axis=1)

        colors_list = ['yellowgreen','orange','dodgerblue','red','rebeccapurple','black']
        try:
            colors = colors_list[0:len(fractions)]
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
                ax.text(x, y, str(int(c)), ha='center', va='center'
                        )#color=text_color)
        ax.legend(ncol=len(descriptionList), bbox_to_anchor=(0, -0.1),
                  loc='lower left', fontsize='small')
