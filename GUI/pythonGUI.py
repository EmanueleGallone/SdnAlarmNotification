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
from GUI.firstPlot import Plot1
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import time
import random
import sqlite3
import logging

#plt.ion()

def organizeData(results):
    for row in results:
        alarmsPerHostDict[row[1]][row[2]] += 1
        totalAlarmsPerSeverityDict[int(row[2])] += 1
    config_manager = ConfigManager()
    severity_levels = config_manager.get_severity_levels()
    for key, item in severity_levels.items():
        for host in alarmsPerHostDict:
            if str(item) not in alarmsPerHostDict[host]:
                alarmsPerHostDict[host][str(item)]=0
        if item not in totalAlarmsPerSeverityDict:
            totalAlarmsPerSeverityDict[item]=0

class DBWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(DBWindow, self).__init__(*args, **kwargs)
        self.title = 'Alarm Table Window'
        self.left =30
        self.top = 30
        self.width = 1300
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
        self.refreshButton.move(650,5)

        self.plotWidget=Plot1(self, width=5.5, height=5.5, dpi=100,updateCheck=False,alarmsPerHost=alarmsPerHostDict,totalAlarmsPerSeverity=totalAlarmsPerSeverityDict)
        self.plotWidget.move(0,30)

        self.plotWidget2=plot2(self, width=8, height=6, dpi=100,updateCheck=False)
        self.plotWidget2.move(560,30)

        #self.plotWidget2=plot1(self, width=5, height=5, dpi=100,updateCheck=False)
        #self.plotWidget2.move(3,3)

        # inizializzo lo spazio dove mettero la tabella
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(230, 140, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText("Empty table")
        #self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def reFresh(self):
        self.plotWidget.axes.cla()
        self.plotWidget.updateCheck=True
        self.plotWidget.reStartPlot1()

        self.plotWidget.alarmsPerHost=alarmsPerHostDict
        self.plotWidget.totalAlarmsPerSeverity=totalAlarmsPerSeverityDict

        self.plotWidget2.axes.cla()
        self.plotWidget2.updateCheck=True
        self.plotWidget2.reStartPlot2()

        self.plotWidget.draw()
        self.plotWidget2.draw()

class plot2(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100,updateCheck=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        #self.fig.tight_layout()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.updateCheck=updateCheck #TODO
        self.barGraph(self.axes)

    def barGraph(self,axes):
        print("here")
        try:
            print("dhere")
            connection = sqlite3.connect('local.db')
            query = "SELECT deviceIP FROM alarm"
            result = connection.execute(query)
            alarms_ip = []
            for column_number, data in enumerate(result):
                alarms_ip.append(data[0])
            labels = set(alarms_ip)

            query = "SELECT description FROM alarm"
            result = connection.execute(query)
            alarms_desc = []
            for column_number, data in enumerate(result):
                alarms_desc.append(data[0])
            alarms_description = set(alarms_desc)

            rects=[]
            for alarms in alarms_description:
                means = []
                for ip in labels:
                    t=(alarms,)
                    query = "SELECT COUNT() FROM "+"alarm WHERE DESCRIPTION=? AND deviceIP='"+str(ip)+"'"
                    result = connection.execute(query, t)
                    for column_number, data in enumerate(result):

                        if self.updateCheck == True:
                            means.append(data[0]+random.randint(3,10))
                        else:
                            means.append(data[0])

                rects.append(means)

            #print(alarms_description)
            print(rects)

            x = np.arange(len(labels))  # the label locations
            width = 0.2  # the width of the bars
            i=0
            for i in range(0, len(rects)):

                bar= axes.bar(x + (i-(len(rects)-1)/2) * width / 2, rects[i], width/2, label=list(alarms_description)[i])
                autolabel(bar,axes)
                print(rects[i])
            # Add some text for labels, title and custom x-axis tick labels, etc.
            axes.set_ylabel('Number of Alarms')
            axes.set_title('Alarms by IP')
            axes.set_xticks(x)
            axes.set_xticklabels(labels)
            axes.legend(loc='best', bbox_to_anchor= (0.5,0.,0.5,0.5))
            connection.close()
            #plt.show()
        except Exception as e:
            logging.log(logging.ERROR, "something wrong opening the Data Base" + str(e))
    def reStartPlot2(self):
        self.barGraph(self.axes)

def autolabel(rects,axes):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        axes.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def redoRefresh():
    results = fetchDataFromDB()
    print("Here I need to implement the refresh code")
    alarmsPerHostDict.clear()
    totalAlarmsPerSeverityDict.clear()
    organizeData(results)
    Gui.reFresh()


def fetchDataFromDB():
    alarmTable = DBHandler()
    alarmTable.open_connection()
    results = alarmTable.select_all()
    alarmTable.close_connection()
    return results

results = fetchDataFromDB()
alarmsPerHostDict=defaultdict(lambda: defaultdict(int)) #stores IPAddress and the correspondents severity alarms counters
totalAlarmsPerSeverityDict=defaultdict(int) #defaultdict(int)=inizializza il dizionario a 0

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

    for host in alarmsPerHostDict:
        print(host)
        xlistElements, ylistElements = [], []
        #lbl = "Host:s{0}".format(host)  # Labels: (s1, s2), (s2,s3), etc.
        for severity in sorted(alarmsPerHostDict[host].keys()):

            #x_max = len(sedge_stats[host].src_port_stats['throughputs_array'])

            #links_labels.append(lbl)
            #print(alarmsPerHostDict[host]," ",alarmsPerHostDict[host][severity],"  ",severity)

            xlistElements.append(int(severity))
            ylistElements.append(alarmsPerHostDict[host][severity])
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
