# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
import sys
from GUI.commonPlotFunctions import CommonFunctions
from GUI.firstPlot import Plot1
from GUI.secondPlot import Plot2
from GUI.horizontalBarGraph import HorizontalGraph

from collections import defaultdict

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
        self.refreshButton.move(200,5)


        self.plotWidget=Plot1(self, width=5.5, height=4, dpi=100,updateCheck=False)
        self.plotWidget.move(0,30)

        self.plotWidget2=Plot2(self, width=7, height=5, dpi=100,updateCheck=False)
        self.plotWidget2.move(560,0)

        self.plotWidget3=HorizontalGraph(self, width=13, height=5, dpi=100,updateCheck=False)
        self.plotWidget3.move(0,500)

        QtCore.QMetaObject.connectSlotsByName(self)

    def reFresh(self):

        self.plotWidget.axes.cla()
        self.plotWidget.updateCheck=True
        self.plotWidget.reStartPlot1()

        self.plotWidget2.axes.cla()
        self.plotWidget2.updateCheck=True
        self.plotWidget2.reStartPlot2()



        self.plotWidget3.axes.cla()
        self.plotWidget3.updateCheck = True
        self.plotWidget3.reStartPlot3()


        self.plotWidget.draw()
        self.plotWidget2.draw()
        self.plotWidget3.draw()

def clickRefreshButtonEvent():
    Gui.reFresh()


app = QtWidgets.QApplication([])
Gui = DBWindow()
Gui.refreshButton.clicked.connect(clickRefreshButtonEvent)

Gui.show()

app.exec_()


sys.exit(app.exec())
