# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HelloWorldWindow(object):
    def setupUi(self, HelloWorldWindow):
        HelloWorldWindow.setObjectName("HelloWorldWindow")
        HelloWorldWindow.resize(706, 600)
        self.centralwidget = QtWidgets.QWidget(HelloWorldWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.pushButton.raise_()
        self.checkBox.raise_()
        self.pushButton_2.raise_()
        self.label.raise_()
        HelloWorldWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(HelloWorldWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 706, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        HelloWorldWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(HelloWorldWindow)
        self.statusbar.setObjectName("statusbar")
        HelloWorldWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(HelloWorldWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(HelloWorldWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(HelloWorldWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(HelloWorldWindow)
        QtCore.QMetaObject.connectSlotsByName(HelloWorldWindow)

    def retranslateUi(self, HelloWorldWindow):
        _translate = QtCore.QCoreApplication.translate
        HelloWorldWindow.setWindowTitle(_translate("HelloWorldWindow", "MainWindow"))
        self.pushButton.setText(_translate("HelloWorldWindow", "PushButton"))
        self.checkBox.setText(_translate("HelloWorldWindow", "CheckBox"))
        self.label.setText(_translate("HelloWorldWindow", "Layout garantisce resize  objectName è il nome della variabile su python"))
        self.pushButton_2.setText(_translate("HelloWorldWindow", "PushButton"))
        self.menuFile.setTitle(_translate("HelloWorldWindow", "File"))
        self.menuSettings.setTitle(_translate("HelloWorldWindow", "Settings"))
        self.actionOpen.setText(_translate("HelloWorldWindow", "Open"))
        self.actionSave.setText(_translate("HelloWorldWindow", "Save"))
        self.actionExit.setText(_translate("HelloWorldWindow", "Exit"))
