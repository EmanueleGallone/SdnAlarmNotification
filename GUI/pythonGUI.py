# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
import sys
from models.database_handler import DBHandler
from models.config_manager import ConfigManager
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import time
import random

#plt.ion()

def organizeData(results):
    for row in results:
        alarmsPerHost[row[1]][row[2]] += 1
        totalAlarmsPerSeverity[row[2]] += 1
    config_manager = ConfigManager()
    severity_levels = config_manager.get_severity_levels()
    for key, item in severity_levels.items():
        for host in alarmsPerHost:
            if str(item) not in alarmsPerHost[host]:
                alarmsPerHost[host][str(item)]=0

class plot1(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100,updateCheck=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.updateCheck=updateCheck
        self.plotCode(self.axes,True)

    def position(self,ax):
        width=0.25
        i=0
        odd=True
        even=False

        for host in alarmsPerHost:
            xlistElements, ylistElements,descriptionList,loc = [], [],[],[]
            lbl = "Host:{0}".format(host)  # Labels: (s1, s2), (s2,s3), etc.
            if i % 2 == 0:
                if even==False:
                    even=True
                    deltaPosition = +width * i
                else:
                    deltaPosition = -width * i
                    odd = True
            else:
                if odd==False:
                    odd=True
                    deltaPosition = -width * i
                else:
                    deltaPosition = +width * i
                    even = True
            for severity in sorted(alarmsPerHost[host].keys()):
                loc.append(int(severity) +deltaPosition)
                xlistElements.append(int(severity))
                if self.updateCheck==True:
                    tot=alarmsPerHost[host][severity]+random.randint(10,100)
                    ylistElements.append(tot)
                    print(tot,"ooo",alarmsPerHost[host][severity])
                else:
                    ylistElements.append(alarmsPerHost[host][severity])

                ax.annotate(alarmsPerHost[host][severity],xy=(int(severity) + deltaPosition - width / 5, alarmsPerHost[host][severity] + 0.15))
                plt.annotate(alarmsPerHost[host][severity], xy=(int(severity) +deltaPosition-width/5, alarmsPerHost[host][severity]+0.15))
            #plt.plot(xlistElements, ylistElements,'-',label=lbl,marker='o')
            ax.bar(loc, ylistElements, label=lbl, width=0.2)
            plt.bar(loc, ylistElements, label=lbl, width=0.2)
            print("position ")
            descriptionList=self.getInfo(xlistElements)
            #print(descriptionList)
            ax.set_xticks(xlistElements)
            ax.set_xticklabels(descriptionList)
            plt.xticks(xlistElements,descriptionList)
            #plt.setp(ax,xlistElements,descriptionList,ylistElements)
            if odd and even:
                i=i+1
                odd=False
                even=False

    def plotCode(self,ax,new):
        if(new==True):
            ax.set_xlabel("Severity Level")
            ax.set_ylabel("Number of alarms")
            ax.set_title("Alarms received per host ")
        self.position(ax)
        print("plotcode ")

        ax.axhline(7, color='black', linestyle='--',label="num threshold")
        plt.axhline(7, color='black', linestyle='--', label="num threshold")
        ax.legend()
        plt.legend()

        #plt.show()


    def reStart(self):
        #self.clearFigure(self.fig)
        self.plotCode(self.axes,False)

    def clearFigure(self,oldFigure):
        fig = oldFigure
        fig.canvas.draw_idle()
        time.sleep(0.01)  # sleep + flush_events invece che pause, secondo stackOverflow e' meglio, piu' efficiente
        fig.canvas.flush_events()

    def getInfo(self,xlistElements):
        _config_manager = ConfigManager()
        descriptionList = []
        for element in xlistElements:
            descriptionList.append(_config_manager.get_severity_mapping(element))
        return descriptionList
#https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py

class DBWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(DBWindow, self).__init__(*args, **kwargs)
        self.title = 'Alarm Table Window'
        self.left =30
        self.top = 30
        self.width = 1200
        self.height = 700
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #creo un widget (praticamente la mia finestra)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        #inizializzo il refresh button :QPushButton:https://doc.qt.io/qt-5/qpushbutton.html
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(700, 1500, 75, 23))
        self.refreshButton.setObjectName("refreshButton") #variable name
        self.refreshButton.setText("Refresh")  #name that appears in the window
        self.refreshButton.setStatusTip("Click this if you want to re-Fresh the table")
        self.refreshButton.setCheckable(True) #by default is unchecked
        self.refreshButton.move(600,600)

        self.plotWidget=plot1(self, width=5, height=5, dpi=100,updateCheck=False)
        self.plotWidget.move(0,0)

        # inizializzo lo spazio dove mettero la tabella
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(230, 140, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText("Empty table")
        #self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
    def reStartGui(self):
        self.plotWidget.axes.cla()
        self.plotWidget.updateCheck=True
        self.plotWidget.reStart()
        self.plotWidget.draw()

def redoRefresh():
    results = fetchDataFromDB()
    print("Here I need to implement the refresh code")
    alarmsPerHost.clear()
    totalAlarmsPerSeverity.clear()
    organizeData(results)
    Gui.reStartGui()


def fetchDataFromDB():
    alarmTable = DBHandler()
    alarmTable.open_connection()
    results = alarmTable.select_all()
    alarmTable.close_connection()
    return results

results = fetchDataFromDB()
alarmsPerHost=defaultdict(lambda: defaultdict(int)) #stores IPAddress and the correspondents severity alarms counters
totalAlarmsPerSeverity=defaultdict(int) #defaultdict(int)=inizializza il dizionario a 0

organizeData(results)

app = QtWidgets.QApplication([])
Gui = DBWindow()
Gui.refreshButton.clicked.connect(redoRefresh)

Gui.show()

app.exec_()


sys.exit(app.exec())




'''
def plot1():
    """Flow's throughput on each link: table and histogram."""

   # fig.canvas.set_window_title("Alarms notifications")
    #ax = fig.add_subplot(111)
    # Clear the current figure
    #fig.clf()
    #ax = fig.add_subplot(111)
    rows_labels = self.table_rows_labels
    columns_labels = self.table_columns_labels
    columns_labels = tuple(columns_labels)
    data = self.table_data
    y_values = np.arange(0, (LINK_THRESHOLD*1.5)/MAGNITUDE, (LINK_THRESHOLD/5)/MAGNITUDE)
    n_rows = len(data)
    x_ax = np.arange(len(columns_labels))
    bar_width = 0.4
    spare_width = (1 - bar_width)/2
    # Initialize the vertical-offset for the stacked bar chart
    y_offset = np.zeros(len(columns_labels))

    #plt.subplot(2,1,1)


    xlistElements,ylistElements=[],[]

    #ax.set_xlabel("Severity Level")
    #ax.set_ylabel("Number of alarms")

    for host in alarmsPerHost:
        print(host)
        xlistElements, ylistElements = [], []
        #lbl = "Host:s{0}".format(host)  # Labels: (s1, s2), (s2,s3), etc.
        for severity in sorted(alarmsPerHost[host].keys()):

            #x_max = len(sedge_stats[host].src_port_stats['throughputs_array'])

            #links_labels.append(lbl)
            #print(alarmsPerHost[host]," ",alarmsPerHost[host][severity],"  ",severity)

            xlistElements.append(int(severity))
            ylistElements.append(alarmsPerHost[host][severity])
            # ax.legend(fancybox=True, framealpha=0.5)        # Slows down the program
            #tmp_links_usg.append(self.edge_stats[link].src_port_stats['throughputs_array'])  # To print the peak
        plt.plot(xlistElements, ylistElements,'-',label=host,marker='o')
    #print(xlistElements," ", ylistElements)
    #plt.plot(xlistElements, ylistElements,'-',lw=2)
    plt.axhline(4,color='black', linestyle='--')

    plt.xlabel("Severity Level")
    plt.ylabel("Number of alarms")
    plt.title("Alarms received per host ")
    plt.legend()
    plt.show()

    plt.subplot(2, 1, 2)
    plt.plot([7,8,9], [5,6,7],'-',lw=2)
    plt.xlabel("Severity Level")
    plt.ylabel("Number of alarms")
    plt.title("see")
    plt.show() //just once 
    #ax.axhline(7, color='black', linestyle='--')
'''
