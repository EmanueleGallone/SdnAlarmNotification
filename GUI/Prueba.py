# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Prueba.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import numpy as np
import random
import json

#from main import main

import sqlite3
import logging

from GUI.firstPlot import Plot1
from GUI.secondPlot import Plot2
from GUI.horizontalBarGraph import HorizontalGraph

Notification=['']*6
Ip=['']*4

class Ui_MainWindow(object):
#######################################################################
    def loadDataB(self):
        try:
            from models import database_handler
            db = database_handler.DBHandler().open_connection()
            result = [tuple for tuple in db.select_all()]

            # connection = sqlite3.connect('local.db')
            # query = "SELECT * FROM alarm"
            # result = connection.execute(query)

            self.tableWidget.setRowCount(0)
            self.tableWidget.setVisible(True)
            self.tableWidget.horizontalHeader().setVisible(True)
            self.tableWidget.setHorizontalHeaderLabels(
                ["Alarm", "DeviceIP", "Severity", "Description", "Time", "Notified", "Ceased"])

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

            db.close_connection()
        except Exception as e:
            logging.log(logging.ERROR, "something wrong opening the Data Base" + str(e))
########################################################################################
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
########################################################################################
    def get_credentials(self):
        Notification[0]=(self.Send_Mail.displayText())
        self.Send_Mail.clear()
        Notification[1]=(self.Password.text())
        self.Password.clear()
        Notification[2]=(self.Reciver_Mail.displayText())
        self.Reciver_Mail.clear()
        Notification[3]=(self.Severity.value())
        self.Severity.clear()
        Notification[4]=(self.Mail_Button.isChecked())
        self.Mail_Button.setChecked(False)
        Notification[5]=(self.Message_Button.isChecked())
        self.Message_Button.setChecked(False)
        #print(Notification)
    def get_Network(self):
        Ip[0]=(self.Ip_19.isChecked())
        self.Ip_19.setChecked(False)
        Ip[1]=(self.Ip_21.isChecked())
        self.Ip_21.setChecked(False)
        Ip[2]=(self.Ip_23.isChecked())
        self.Ip_23.setChecked(False)
        Ip[3]=(int(self.Fetch_sec.value()))
        self.Fetch_sec.clear()
        #print(Ip)
########################################################################################
    def modify_json(self):
        try:
            import os
            filename = os.path.join(os.path.dirname(__file__), '../config/config.json')

            with open(filename, 'r') as json_file:
                data = json.load(json_file)
                try:
                    with open('config.json', 'w') as json_file:

                        data['Notification_config']['Sender_email'] = Notification[0]
                        data['Notification_config']['Sender_email_password'] = Notification[1]
                        data['Notification_config']['Receiver_Email'] = Notification[2]
                        data['Notification_config']['Severity_notification_threshold'] = Notification[3]
                        data['Notification_config']['Send_email'] = Notification[4]
                        data['Notification_config']['Send_message'] = Notification[5]

                        for i in range(len(Ip)-2,-1,-1):
                            if Ip[i]:
                                data['Network'][i]['netconf_fetch_rate_in_sec'] = Ip[3]
                            else:
                                data['Network'].pop(i)

                        json.dump(data, json_file, indent=4, sort_keys=True)

                        self.Run()
                except Exception as e:
                    logging.log(logging.CRITICAL, "Error writing config.json file! -> " + str(e))
        except Exception as e:
            logging.log(logging.CRITICAL, "Error reading config.json file! -> " + str(e))
########################################################################################
    def show_popup(self,notif,ip):
        msg = QMessageBox()
        msg.setWindowTitle("Verify Configuration")
        msg.setText("Configurations where not selected:")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry | QMessageBox.Ignore )
        msg.setDefaultButton(QMessageBox.Retry)
        msg.setInformativeText("Press Ignore if you want to use the default configuration")
        if notif:
            if ip:
                msg.setDetailedText("Neither notification or network configurations were selected")
            else:
                msg.setDetailedText("Notification configurations were not selected")
        elif ip:
                msg.setDetailedText("Network configurations were not selected")
        msg.exec()
        if msg.clickedButton().text() == "Ignore":
            self.Run()
########################################################################################
    def Verification(self):
        notif=all(elem == Notification[0] for elem in Notification)
        ip=all(elem == Ip[0] for elem in Ip)
        if notif or ip:
            self.show_popup(notif,ip)
        else:
            self.modify_json()
##########################################################################################
    def Run(self):
        print("run")
        # main.main()
        self.formGroupBox.setEnabled(False)
        self.button_credentials.setEnabled(False)
        self.formGroupBox2.setEnabled(False)
        self.button_Ip.setEnabled(False)
        self.button_Json.setEnabled(False)
        self.load_db.setEnabled(True)
        self.button_pie_chart.setEnabled(True)
        #self.button_bar_graph.setEnabled(True)
        self.tab_2.setEnabled(True)
        self.tab_3.setEnabled(True)
        self.tab_4.setEnabled(True)
        self.tab_5.setEnabled(True)
        self.refreshButton.setEnabled(True)

################################################################################
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
###############################################################################
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_2.setEnabled(False)

        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_3.setEnabled(False)

        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_4.setEnabled(False)

        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_5.setEnabled(False)
#################################################################################
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 10, 400, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 40, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(40, 100, 411, 276))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        self.load_db = QtWidgets.QPushButton(self.tab)
        self.load_db.setGeometry(QtCore.QRect(210, 385, 75, 23))
        self.load_db.setObjectName("load_db")
        self.load_db.setEnabled(False)

        self.button_credentials = QtWidgets.QPushButton(self.tab)
        self.button_credentials.setGeometry(QtCore.QRect(730, 270, 110, 20))
        self.button_credentials.setObjectName("button_credentials")

        self.button_Ip = QtWidgets.QPushButton(self.tab)
        self.button_Ip.setGeometry(QtCore.QRect(730, 415, 110, 20))
        self.button_Ip.setObjectName("button_Ip")

        self.button_Json = QtWidgets.QPushButton(self.tab)
        self.button_Json.setGeometry(QtCore.QRect(490, 420, 110, 20))
        self.button_Json.setObjectName("button_Json")

        self.refreshButton = QtWidgets.QPushButton(self.tab)
        self.refreshButton.setGeometry(QtCore.QRect(490, 500, 110, 20))
        self.refreshButton.setObjectName("button_refreash")
        self.refreshButton.setEnabled(False)

        ##################################################################################

        self.Send_Mail = QLineEdit()
        self.Password = QLineEdit()
        self.Password.setEchoMode(2)
        self.Reciver_Mail = QLineEdit()
        self.Severity = QSpinBox()
        self.Severity.setMaximum(3)
        self.Mail_Button= QCheckBox()
        self.Mail_Button.setAutoExclusive(False)
        self.Message_Button = QCheckBox()
        self.Message_Button.setAutoExclusive(False)

        self.formGroupBox = QGroupBox(self.tab)
        self.formGroupBox.setGeometry(QtCore.QRect(630, 100, 300, 160))
        layout = QFormLayout()
        layout.addRow(QLabel("Sender_email:"), self.Send_Mail)
        layout.addRow(QLabel("Password:"), self.Password)
        layout.addRow(QLabel("Receiver_Email:"), self.Reciver_Mail)
        layout.addRow(QLabel("Severity Threshold:"), self.Severity)
        layout.addRow(QLabel("Send E-mail:"), self.Mail_Button)
        layout.addRow(QLabel("Send Message:"), self.Message_Button)
        self.formGroupBox.setLayout(layout)

        ##################################################################################

        self.Ip_19 = QCheckBox()
        self.Ip_19.setAutoExclusive(False)
        self.Ip_21 = QCheckBox()
        self.Ip_21.setAutoExclusive(False)
        self.Ip_23 = QCheckBox()
        self.Ip_23.setAutoExclusive(False)
        self.Fetch_sec = QSpinBox()
        self.Fetch_sec.setMaximum(10)

        self.formGroupBox2 = QGroupBox(self.tab)
        self.formGroupBox2.setGeometry(QtCore.QRect(630, 300, 300, 105))
        layout2 = QFormLayout()
        layout2.addRow(QLabel("10.11.12.19:"), self.Ip_19)
        layout2.addRow(QLabel("10.11.12.21:"), self.Ip_21)
        layout2.addRow(QLabel("10.11.12.23:"), self.Ip_23)
        layout2.addRow(QLabel("Fetch Rate:"), self.Fetch_sec)
        self.formGroupBox2.setLayout(layout2)

        ######################################################################################3

        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()
        self.load_db.clicked.connect(self.loadDataB)

        self.button_credentials.clicked.connect(self.get_credentials)
        self.button_Ip.clicked.connect(self.get_Network)
        self.button_Json.clicked.connect(self.Verification)
        self.refreshButton.clicked.connect(self.reFresh)

        self.plotWidget = Plot1(self.tab_2, width=10, height=4, dpi=100, updateCheck=False)
        self.plotWidget.move(0, 30)
        self.plotWidget2 = Plot2(self.tab_3, width=10, height=4, dpi=100, updateCheck=False)
        self.plotWidget2.move(0, 30)
        self.plotWidget3 = HorizontalGraph(self.tab_4, width=10, height=4, dpi=100, updateCheck=False)
        self.plotWidget3.move(20, 30)
        ###########################
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 918, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Smart Networks and Service Orchestration"))
        self.label_2.setText(_translate("MainWindow", "Alarm Management"))
        self.load_db.setText(_translate("MainWindow", "Load Table"))
        self.button_credentials.setText(_translate("MainWindow", "Notification"))
        self.button_Ip.setText(_translate("MainWindow", "Network"))
        self.button_Json.setText(_translate("MainWindow", "Run"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh ALL graphs"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Home"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Graph 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Graph 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Graph 3"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Graph 4"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
