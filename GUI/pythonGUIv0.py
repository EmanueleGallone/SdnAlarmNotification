# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
import sys


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
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
        self.setupUi()

    def setupUi(self):
        #creo un widget (praticamente la mia finestra)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        #dico dove sto mettendo questi elementi
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



Gui.show()

app.exec_()


#Gui.setupUi(w)
#Gui.retranslateUi(w)

sys.exit(app.exec())
'''app = QtWidgets.QApplication([])

win = uic.loadUi("input.ui") #specify the location of your .ui file

win.show()

sys.exit(app.exec())
'''