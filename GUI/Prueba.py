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

Notification=[""]*6
Ip=[""]*4

class Ui_MainWindow(object):
#######################################################################
    def loadDataB(self):
        try:
            connection = sqlite3.connect('local.db')
            query = "SELECT * FROM alarm"
            result = connection.execute(query)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setVisible(True)
            self.tableWidget.horizontalHeader().setVisible(True)
            self.tableWidget.setHorizontalHeaderLabels(
                ["Alarm", "DeviceIP", "Severity", "Description", "Time", "Notified", "Ceased"])

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

            connection.close()
        except Exception as e:
            logging.log(logging.ERROR, "something wrong opening the Data Base" + str(e))
    ##############################################################################
    def Pie_chart(self):
        try:
            connection = sqlite3.connect('local.db')
            query = "SELECT deviceIP FROM alarm"
            result = connection.execute(query)
            alarms_ip = []
            for column_number, data in enumerate(result):
                alarms_ip.append(data[0])
            labels = set(alarms_ip)
            sizes = [alarms_ip.count(i) for i in labels]

            # make figure and assign axis objects
            fig = plt.figure(figsize=(11, 4))
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            fig.subplots_adjust(wspace=0)

            # pie chart parameters
            explode = [0, 0, 0]
            explode[sizes.index(max(sizes))] = 0.1
            ax1.pie(sizes, autopct='%1.1f%%',
                    labels=labels, explode=explode)

            # bar chart parameters
            query = "SELECT description FROM alarm"
            result = connection.execute(query)
            alarms_description = []
            for column_number, data in enumerate(result):
                alarms_description.append(data[0])
            labels = set(alarms_description)
            sizes = [alarms_description.count(i) for i in labels]

            xpos = 0
            bottom = 0
            width = .1

            for j in range(len(sizes)):
                height = sizes[j]
                ax2.bar(xpos, height, width, bottom=bottom)
                ypos = bottom + ax2.patches[j].get_height() / 2
                bottom += height
                ax2.text(xpos, ypos, str(sizes[j]),
                         ha='center')

            ax2.set_title('All Alarms Description')
            ax2.legend(labels)
            ax2.axis('off')
            ax2.set_xlim(-width, 5*width)

            plt.show()
            connection.close()
        except Exception as e:
            logging.log(logging.ERROR, "something wrong opening the Data Base" + str(e))
    ###################################################################################
    def Bar_Graph(self):
        try:
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
                        means.append(data[0])
                rects.append(means)

            #print(alarms_description)
            #print(rects)

            x = np.arange(len(labels))  # the label locations
            width = 0.2  # the width of the bars
            fig, ax = plt.subplots()

            def autolabel(rects):
                """Attach a text label above each bar in *rects*, displaying its height."""
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            for i in range(0, len(rects)):
                bar= ax.bar(x + (i-(len(rects)-1)/2) * width / 2, rects[i], width/2, label=list(alarms_description)[i])
                autolabel(bar)

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('Number of Alarms')
            ax.set_title('Alarms by IP')
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend()
            fig.tight_layout()
            connection.close()
            plt.show()
        except Exception as e:
            logging.log(logging.ERROR, "something wrong opening the Data Base" + str(e))
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
        print(Notification)
    def get_Network(self):
        Ip[0]=(self.Ip_19.isChecked())
        self.Ip_19.setChecked(False)
        Ip[1]=(self.Ip_21.isChecked())
        self.Ip_21.setChecked(False)
        Ip[2]=(self.Ip_23.isChecked())
        self.Ip_23.setChecked(False)
        Ip[3]=(int(self.Fetch_sec.value()))
        self.Fetch_sec.clear()
        print(Ip)
########################################################################################
    def modify_json(self):
        try:
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)
                try:
                    with open('config.json', 'w') as json_file:

                        data['Notification_config']['Sender_email'] = Notification[0]
                        data['Notification_config']['Sender_email_password'] = Notification[1]
                        data['Notification_config']['Receiver_Email'] = Notification[2]
                        data['Notification_config']['Severity_notification_threshold'] = Notification[3]
                        data['Notification_config']['Send_email'] = Notification[4]
                        data['Notification_config']['Send_message'] = Notification[5]
                        data['Network'][0]['netconf_fetch_rate_in_sec']=Ip[3]
                        data['Network'][1]['netconf_fetch_rate_in_sec'] = Ip[3]
                        data['Network'][2]['netconf_fetch_rate_in_sec'] = Ip[3]
                        json.dump(data, json_file, indent=4, sort_keys=True)
                except Exception as e:
                    logging.log(logging.CRITICAL, "Error writing config.json file! -> " + str(e))
        except Exception as e:
            logging.log(logging.CRITICAL, "Error reading config.json file! -> " + str(e))
########################################################################################
    def Run_All(self):
        print("run")
        #main.main()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 10, 411, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 40, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(40, 100, 411, 276))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        self.load_db = QtWidgets.QPushButton(self.centralwidget)
        self.load_db.setGeometry(QtCore.QRect(210, 385, 75, 23))
        self.load_db.setObjectName("load_db")

        self.button_pie_chart = QtWidgets.QPushButton(self.centralwidget)
        self.button_pie_chart.setGeometry(QtCore.QRect(490, 100, 110, 20))
        self.button_pie_chart.setObjectName("button_pie_chart")

        self.button_bar_graph = QtWidgets.QPushButton(self.centralwidget)
        self.button_bar_graph.setGeometry(QtCore.QRect(490, 130, 110, 20))
        self.button_bar_graph.setObjectName("button_bar_graph")

        self.button_credentials = QtWidgets.QPushButton(self.centralwidget)
        self.button_credentials.setGeometry(QtCore.QRect(730, 270, 110, 20))
        self.button_credentials.setObjectName("button_credentials")

        self.button_Ip = QtWidgets.QPushButton(self.centralwidget)
        self.button_Ip.setGeometry(QtCore.QRect(730, 415, 110, 20))
        self.button_Ip.setObjectName("button_Ip")

        self.button_Json = QtWidgets.QPushButton(self.centralwidget)
        self.button_Json.setGeometry(QtCore.QRect(490, 420, 110, 20))
        self.button_Json.setObjectName("button_Json")

        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(490, 450, 110, 20))
        self.Run.setObjectName("Run")

        ##################################################################################

        self.Send_Mail = QLineEdit()
        self.Password = QLineEdit()
        self.Password.setEchoMode(2)
        self.Reciver_Mail = QLineEdit()
        self.Severity = QSpinBox()
        self.Severity.setMaximum(3)
        self.Mail_Button= QRadioButton()
        self.Mail_Button.setAutoExclusive(False)
        self.Message_Button = QRadioButton()
        self.Message_Button.setAutoExclusive(False)

        self.formGroupBox = QGroupBox(self.centralwidget)
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

        self.Ip_19 = QRadioButton()
        self.Ip_19.setAutoExclusive(False)
        self.Ip_21 = QRadioButton()
        self.Ip_21.setAutoExclusive(False)
        self.Ip_23 = QRadioButton()
        self.Ip_23.setAutoExclusive(False)
        self.Fetch_sec = QSpinBox()
        self.Fetch_sec.setMaximum(10)

        self.formGroupBox2 = QGroupBox(self.centralwidget)
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

        self.button_pie_chart.clicked.connect(self.Pie_chart)
        self.button_bar_graph.clicked.connect(self.Bar_Graph)
        self.button_credentials.clicked.connect(self.get_credentials)
        self.button_Ip.clicked.connect(self.get_Network)
        self.button_Json.clicked.connect(self.modify_json)
        self.Run.clicked.connect(self.Run_All)

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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Smart Networks and Service Orchestration"))
        self.label_2.setText(_translate("MainWindow", "Alarm Management"))
        self.load_db.setText(_translate("MainWindow", "Load Table"))
        self.button_pie_chart.setText(_translate("MainWindow", "Generate Pie Chart"))
        self.button_bar_graph.setText(_translate("MainWindow", "Generate Bar Graph"))
        self.button_credentials.setText(_translate("MainWindow", "Insert Credentials"))
        self.button_Ip.setText(_translate("MainWindow", "Select Terminals"))
        self.button_Json.setText(_translate("MainWindow", "Modify Jason"))
        self.Run.setText(_translate("MainWindow", "Run"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
