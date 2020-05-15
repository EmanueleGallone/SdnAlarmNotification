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
import numpy as np


class DBWindow(QMainWindow):
    '''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(490, 400, 75, 23))
        self.refreshButton.setObjectName("refreshButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(130, 410, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(230, 140, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
       # MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtWidgets.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
       # MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExplore = QtWidgets.QAction(MainWindow)
        self.actionExplore.setObjectName("actionExplore")
        self.menuMain.addAction(self.actionSave)
        self.menuMain.addAction(self.actionExplore)
        self.menubar.addAction(self.menuMain.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.refreshButton.setStatusTip("refresh from DB")
        self.refreshButton.triggered.connect(qApp.quit)
        self.menuMain.setTitle(_translate("MainWindow", "Main"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExplore.setText(_translate("MainWindow", "Explore"))
    '''

    def __init__(self, *args, **kwargs):
        super(DBWindow, self).__init__(*args, **kwargs)
        self.title = 'Alarm Table Window'
        self.left =30
        self.top = 30
        self.width = 1200
        self.height = 700
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.show()

        #creo un widget (praticamente la mia finestra)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)


        #inizializzo il refresh button :QPushButton:https://doc.qt.io/qt-5/qpushbutton.html
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(350, 400, 75, 23))
        self.refreshButton.setObjectName("refreshButton") #variable name
        self.refreshButton.setText("Refresh")  #name that appears in the window
        self.refreshButton.setStatusTip("Click this if you want to re-Fresh the table")
        self.refreshButton.setCheckable(True) #by default is unchecked


        #self.refreshButton.toggle()
        '''
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(130, 410, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.refreshButton.setText("Refresh")
        
        '''
        # inizializzo lo spazio dove mettero la tabella
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(230, 140, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText("Empty table")

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtWidgets.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")

        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionExplore = QtWidgets.QAction(self)
        self.actionExplore.setObjectName("actionExplore")
        self.menuMain.addAction(self.actionSave)
        self.menuMain.addAction(self.actionExplore)
        self.menubar.addAction(self.menuMain.menuAction())

        #self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)


app = QtWidgets.QApplication([])
Gui = DBWindow()


alarmTable=DBHandler()

alarmTable.open_connection()
results=alarmTable.select_all()
alarmTable.close_connection()

alarmsPerHost=defaultdict(lambda: defaultdict(int)) #stores IPAddress and the correspondents severity alarms counters
totalAlarmsPerSeverity=defaultdict(int) #defaultdict(int)=inizializza il dizionario a 0

for row in results:
    alarmsPerHost[row[1]][row[2]] += 1
    totalAlarmsPerSeverity[row[2]] += 1
print(results)

#for host in alarmsPerHost:
 #   for severity in alarmsPerHost[host]:
  #      print("")




def plot1():

    for host in alarmsPerHost:

        xlistElements, ylistElements = [], []
        lbl = "Host:{0}".format(host)  # Labels: (s1, s2), (s2,s3), etc.
        for severity in sorted(alarmsPerHost[host].keys()):
            xlistElements.append(int(severity))
            ylistElements.append(alarmsPerHost[host][severity])


        descriptionList=getInfo(xlistElements)
        plt.xticks(xlistElements,descriptionList)
        plt.plot(xlistElements, ylistElements,'-',label=lbl,marker='o')
    plt.axhline(3,color='black', linestyle='--')

    plt.xlabel("Severity Level")
    plt.ylabel("Number of alarms")
    plt.title("Alarms received per host ")
    plt.xlim(-0.5,5.5)
    plt.legend()
    plt.show()


def getInfo(xlistElements):
    _config_manager = ConfigManager()
    descriptionList=[]
    for element in xlistElements:
        descriptionList.append(_config_manager.get_severity_mapping(element))
    return descriptionList

def redoRefresh():
    print("Here I need to implement the refresh code")

Gui.refreshButton.clicked.connect(redoRefresh)


plot1()

Gui.show()

app.exec_()


sys.exit(app.exec())

'''app = QtWidgets.QApplication([])

win = uic.loadUi("input.ui") #specify the location of your .ui file

win.show()

sys.exit(app.exec())
'''



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
