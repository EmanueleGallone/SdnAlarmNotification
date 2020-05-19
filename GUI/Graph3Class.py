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
    def __init__(self, parent=None, width=7.5, height=5, dpi=100, updateCheck=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.fig.patch.set_visible(False)
        FigureCanvas.__init__(self, self.fig)
        self.alarmsPerHost = defaultdict(lambda: defaultdict(int))
        self.totalAlarmsPerSeverity = defaultdict(lambda: [])
        self.percentage=defaultdict(int)
        self.setParent(parent)
        self.updateCheck = updateCheck
        self.axes.invert_yaxis()
        self.axes.xaxis.set_visible(False)
        self.axes.set_title("Percentage of the various alarms ",color='white')

    def plotHOrizontalGraph(self,ax):
        getData = CommonFunctions()
        descriptionList,totalFractions = [],[]
        totAlarms=getData.countAlarms(self.totalAlarmsPerSeverity)

        for key, item in sorted(self.totalAlarmsPerSeverity.items()):
            descriptionList.append(getData.getInfo(key))
            totFraction=item/totAlarms
            totalFractions.append(totFraction*100)

        self.percentage['Overall Alarms'] = totalFractions

        for host in sorted(self.alarmsPerHost):
            singleFractions = []
            totPerHostAlarms=getData.countAlarms(self.alarmsPerHost[host])
            for ele in sorted(self.alarmsPerHost[host]):
                singleFractions.append((self.alarmsPerHost[host][ele]/totPerHostAlarms)*100)
            self.percentage[host] = singleFractions

        labels = list(self.percentage.keys())
        data = np.array(list(self.percentage.values()))
        data_cum = data.cumsum(axis=1)
        colors_list = ['yellowgreen','orange','dodgerblue','red','rebeccapurple','black']

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

    def reStartPlot3(self):
        self.alarmsPerHost.clear()
        self.totalAlarmsPerSeverity.clear()
        self.percentage.clear()
        self.axes.invert_yaxis()
        self.axes.xaxis.set_visible(False)
        self.axes.set_title("Percentage of the various alarms ",color='white')
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')

        getNewData = CommonFunctions()
        results = getNewData.fetchDataFromDB()
        try:
            if (len(results)==0):
                raise Exception("No plot of graph 3")
            self.alarmsPerHost = getNewData.organizeAlarmsPerHost(results)
            self.totalAlarmsPerSeverity = getNewData.organizeTotalAlarmsPerSeverity(results)
            self.plotHOrizontalGraph(self.axes)
        except Exception as e:
            logging.log(logging.ERROR, "The alarm table is empty: " + str(e))

    def saveGraph3(self,directory):
        path = directory + "\Graph3.png"
        try:
            self.fig.savefig(path)
        except Exception as e:
            logging.log(logging.CRITICAL, str(e)+": we cannot save the graph 3 invalid: ")