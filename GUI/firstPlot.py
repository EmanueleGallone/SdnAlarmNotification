
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
import sys
from models.database_manager import DBHandler
from models.config_manager import ConfigManager
from GUI.commonPlotFunctions import CommonFunctions
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import random
import datetime
dirname = os.path.dirname(__file__)



class Plot1(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100, updateCheck=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_visible(False)
        self.axes = self.fig.add_subplot(111)
        # self.axes = self.fig.add_subplot(221)
        # self.axes2 = self.fig.add_subplot(222)
        FigureCanvas.__init__(self, self.fig)
        self.alarmsPerHost = defaultdict(lambda: defaultdict(int)) #stores IPAddress and the correspondents severity alarms counters
        self.totalAlarmsPerSeverity = defaultdict(int) #defaultdict(int)=inizializza il dizionario a 0
        self.setParent(parent)
        self.updateCheck = updateCheck
        #self.plotCode(self.axes)
        self.axes.set_xlabel("Severity Level",color='white')
        self.axes.set_ylabel("Number of alarms",color='white')
        self.axes.set_title("Alarms received per host ",color='white')
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')

    def position(self, ax):
        width = 0.25
        i = 0
        odd = True
        even = False

        for host in self.alarmsPerHost:
            xlistElements, ylistElements, descriptionList, loc = [], [], [], []
            lbl = "Host:{0}".format(host)
            if i % 2 == 0:
                if even == False:
                    even = True
                    deltaPosition = +width * i
                else:
                    deltaPosition = -width * i
                    odd = True
            else:
                if odd == False:
                    odd = True
                    deltaPosition = -width * i
                else:
                    deltaPosition = +width * i
                    even = True
            getData = CommonFunctions()
            for severity in sorted(self.alarmsPerHost[host].keys()):
                loc.append(int(severity) + deltaPosition)
                xlistElements.append(int(severity))

                descriptionList.append(getData.getInfo(int(severity)))

                if self.updateCheck == True:
                    tot = self.alarmsPerHost[host][severity] + random.randint(10, 100)
                    ylistElements.append(tot)
                    # print(tot,"ooo",self.alarmsPerHost[host][severity])
                else:
                    ylistElements.append(self.alarmsPerHost[host][severity])

                ax.annotate(self.alarmsPerHost[host][severity],
                            xy=(int(severity) + deltaPosition - width / 5, self.alarmsPerHost[host][severity] + 0.15),color='white')

                # plt.annotate(self.alarmsPerHost[host][severity], xy=(int(severity) +deltaPosition-width/5, self.alarmsPerHost[host][severity]+0.15))
            # plt.plot(xlistElements, ylistElements,'-',label=lbl,marker='o')
            ax.bar(loc, ylistElements, label=lbl, width=0.2)
            # plt.bar(loc, ylistElements, label=lbl, width=0.2)
            # print("position ")

            # print(descriptionList)
            ax.set_xticks(xlistElements)
            ax.set_xticklabels(descriptionList)
            # plt.xticks(xlistElements,descriptionList)
            # plt.setp(ax,xlistElements,descriptionList,ylistElements)
            if odd and even:
                i = i + 1
                odd = False
                even = False
        infoRefresh = "Last reFresh at time:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ax.text(0, -0.12, infoRefresh, verticalalignment='center',
                transform=ax.transAxes,color='white')


    def plotCode(self, ax):
        ax.set_xlabel("Severity Level",color='white')
        ax.set_ylabel("Number of alarms",color='white')
        ax.set_title("Alarms received per host ",color='white')
        self.position(ax)

        # print("plotcode ")

        yAverageList = []
        xAverageList = []
        for key, item in sorted(self.totalAlarmsPerSeverity.items()):
            avg = item / len(self.alarmsPerHost)#TO do HOST
            #print(round(avg,1))
            yAverageList.append(avg)
            xAverageList.append(int(key))
            ax.annotate(round(avg,1), xy=(key, avg + 0.15))

        ax.plot(xAverageList, yAverageList, color='red', linestyle='--', label="Average number of alarms per severity")

        #ax.axhline(7, color='black', linestyle='--', label="num threshold")
        # plt.axhline(7, color='black', linestyle='--', label="num threshold")
        ax.legend(fancybox=True,framealpha=0.5)
        self.fig.savefig('Graph1.png')
        # plt.legend()

        # plt.show()

    def reStartPlot1(self):
        self.alarmsPerHost.clear()
        self.totalAlarmsPerSeverity.clear()

        getData = CommonFunctions()
        results = getData.fetchDataFromDB()
        self.alarmsPerHost=getData.organizeAlarmsPerHost(results)
        self.totalAlarmsPerSeverity = getData.organizeTotalAlarmsPerSeverity(results)


        self.plotCode(self.axes)

    def saveGraph1(self, directory):
        path=directory+"\graph1.png"
        saveObject=CommonFunctions()
        saveObject.saveSingleGraph(path,self.fig,1)


# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py


