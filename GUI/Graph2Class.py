"""
Author Fabio Carminati , 05-2020
Author Andrés Rodriguez

This class defines the second graph: it describes in details the reasons why the various severity alarms have been generated
by the various hosts

The graph is updated every time the user clicks the RefreshButton on the GUI
(i.e. we redo the plot with the new data retrieved from the local DB)

Documentation of matplotlib has been found on: https://matplotlib.org/3.1.1/index.html
"""
import logging
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import numpy as np
import datetime
from models import database_manager
from GUI.commonPlotFunctions import CommonFunctions
dirname = os.path.dirname(__file__)

logging.basicConfig(filename="../../log.log", level=logging.ERROR)

class Graph2(FigureCanvas):
    def __init__(self, parent=None, width=10, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_visible(False)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.axes.set_xlabel('IP addresses of the hosts',color='white')
        self.axes.set_ylabel('Number of Alarms',color='white')
        self.axes.set_title('Alarms by IP',color='white')
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.text(0.5, 0.5, "No data", horizontalalignment='center', verticalalignment='center', fontsize=20)

    #RefreshButton has been clicked:redo the graph
    def reFreshGraph2(self):

        self.plotGraph2(self.axes)

    def plotGraph2(self,axes):
        axes.set_xlabel('IP addresses of the hosts',color='white')
        axes.set_ylabel('Number of Alarms',color='white')
        axes.set_title('Alarms by IP',color='white')

        try:
            db = database_manager.DBHandler().open_connection()
            result = [tuple[1] for tuple in db.select_all()]
            labels = set(result)

            result = [tuple[3] for tuple in db.select_all()]
            alarms_description = set(result)
            rects = []

            for alarms in alarms_description:
                means = []
                for ip in labels:
                    result = db.select_count_by_device_ip(alarms,ip)
                    means.append(result[0][0])
                rects.append(means)

            x = np.arange(len(labels))  # the label locations
            width = 1.5/len(alarms_description)  # the width of the bars

            for i in range(0, len(rects)):
                bar = axes.bar(x + (i - (len(rects) - 1) / 2) * width / 2, rects[i], width / 2,
                             label=list(alarms_description)[i])
                #Decomment these rows if we want to display above the bars their heights
                #getData = CommonFunctions()
                #getData.autolabel(bar,axes)

            axes.set_xticks(x)
            axes.set_xticklabels(labels)
            axes.legend(fancybox=True,framealpha=0.2)

            infoRefresh = "Last reFresh at time:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            axes.text(0, -0.12, infoRefresh, verticalalignment='center',
                   transform=axes.transAxes,color='white')
            axes.set_ylabel('Number of Alarms')
            axes.set_title('Alarms by IP')
            db.close_connection()

        except Exception as e:
            logging.log(logging.ERROR, "something wrong opening the Data Base" + str(e))

    #The user has required to save either this graph or all the graphs
    def saveGraph2(self, directory):
        path=directory+"\graph2.png"
        saveObject=CommonFunctions()
        saveObject.saveSingleGraph(path,self.fig,2)
