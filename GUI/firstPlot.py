import logging
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
import sys
from models.database_handler import DBHandler
from models.config_manager import ConfigManager
from GUI.commonPlotFunctions import CommonFunctions
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import random
dirname = os.path.dirname(__file__)

logging.basicConfig(filename="../../log.log", level=logging.ERROR)

class Plot1(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100, updateCheck=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # self.axes = self.fig.add_subplot(221)
        # self.axes2 = self.fig.add_subplot(222)
        FigureCanvas.__init__(self, self.fig)
        self.alarmsPerHost = defaultdict(lambda: defaultdict(int)) #stores IPAddress and the correspondents severity alarms counters
        self.totalAlarmsPerSeverity = defaultdict(int) #defaultdict(int)=inizializza il dizionario a 0
        self.setParent(parent)
        self.updateCheck = updateCheck
        #self.plotCode(self.axes)

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
            for severity in sorted(self.alarmsPerHost[host].keys()):
                loc.append(int(severity) + deltaPosition)
                xlistElements.append(int(severity))
                if self.updateCheck == True:
                    tot = self.alarmsPerHost[host][severity] + random.randint(10, 100)
                    ylistElements.append(tot)
                    # print(tot,"ooo",self.alarmsPerHost[host][severity])
                else:
                    ylistElements.append(self.alarmsPerHost[host][severity])

                ax.annotate(self.alarmsPerHost[host][severity],
                            xy=(int(severity) + deltaPosition - width / 5, self.alarmsPerHost[host][severity] + 0.15))
                # plt.annotate(self.alarmsPerHost[host][severity], xy=(int(severity) +deltaPosition-width/5, self.alarmsPerHost[host][severity]+0.15))
            # plt.plot(xlistElements, ylistElements,'-',label=lbl,marker='o')
            ax.bar(loc, ylistElements, label=lbl, width=0.2)
            # plt.bar(loc, ylistElements, label=lbl, width=0.2)
            # print("position ")
            descriptionList = self.getInfo(xlistElements)
            # print(descriptionList)
            ax.set_xticks(xlistElements)
            ax.set_xticklabels(descriptionList)
            # plt.xticks(xlistElements,descriptionList)
            # plt.setp(ax,xlistElements,descriptionList,ylistElements)
            if odd and even:
                i = i + 1
                odd = False
                even = False

    def plotCode(self, ax):
        ax.set_xlabel("Severity Level")
        ax.set_ylabel("Number of alarms")
        ax.set_title("Alarms received per host ")
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
        ax.legend()
        # plt.legend()

        # plt.show()

    def reStartPlot1(self):
        self.alarmsPerHost.clear()
        self.totalAlarmsPerSeverity.clear()

        getData = CommonFunctions()
        results = getData.fetchDataFromDB()

        self.organizeData(results)
        self.plotCode(self.axes)

    def getInfo(self, xlistElements):
        _config_manager = ConfigManager()
        descriptionList = []
        for element in xlistElements:
            descriptionList.append(_config_manager.get_severity_mapping(element))
        return descriptionList

# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py

    def organizeData(self,results):
        for row in results:
            self.alarmsPerHost[row[1]][row[2]] += 1
            self.totalAlarmsPerSeverity[int(row[2])] += 1
        config_manager = ConfigManager()
        severity_levels = config_manager.get_severity_levels()
        for key, item in severity_levels.items():
            for host in self.alarmsPerHost:
                if str(item) not in self.alarmsPerHost[host]:
                    self.alarmsPerHost[host][str(item)] = 0
            if item not in self.totalAlarmsPerSeverity:
                self.totalAlarmsPerSeverity[item] = 0
