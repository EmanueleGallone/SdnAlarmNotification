"""
Author  Fabio Carminati , 05-2020
        Emanuele Gallone
        Andrés Rodriguez

The class MainWindow implements the GUI using PyQt5

This is the script to be run in order to start the Alarm Management project

Documentation of PyQt5 has been found on: https://doc.qt.io/qt-5/index.html
"""
#Import Pyqt5 Tools
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import *
#Import Graphic files
from GUI.Graph1Class import Graph1
from GUI.Graph2Class import Graph2
from GUI.Graph3Class import Graph3
from GUI.BreezeStyleSheets import breeze_resources
#Connecting with the main code
from services.main_service import main as Main_Service
import threading

import json
import logging
import os
from models import config_manager

#ICONS
alarm_icon = os.path.join(os.path.dirname(__file__), 'alarm_icon.png')
exit_icon = os.path.join(os.path.dirname(__file__), 'exit.png')
floppy_icon = os.path.join(os.path.dirname(__file__), 'floppy_disk.png')


#Global Variables for modify Json
Notification=['']*6
Device=['']*5

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(MainWindow)
    #Load Table Button
    def loadDataB(self):
        try:
            #Import Data Base
            from models import database_manager
            db = database_manager.DBHandler().open_connection()
            result = [tuple for tuple in db.select_all()]
            #Defining table widget
            self.tableWidget.setRowCount(0)
            self.tableWidget.setVisible(True)
            self.tableWidget.horizontalHeader().setVisible(True)
            self.tableWidget.setHorizontalHeaderLabels(
                ["Alarm", "DeviceIP", "Severity", "Description", "Time", "Notified", "Ceased"])
            #Insert Data on table
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

            db.close_connection()
        except Exception as e:
            logging.log(logging.ERROR, "something wrong opening the Data Base" + str(e))
    #Refresh Button
    def reFresh(self):

        self.plotWidget1.axes.cla()
        self.plotWidget1.reFreshGraph1()

        self.plotWidget2.axes.cla()
        self.plotWidget2.reFreshGraph2()

        self.plotWidget3.axes.cla()
        self.plotWidget3.reFreshGraph3()

        self.plotWidget1.draw()
        self.plotWidget2.draw()
        self.plotWidget3.draw()
    #Save Notification information
    def Json_Notification(self):
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
    # Save Network information
    def Json_Network(self):
        Device[0] = (self.device_ip.displayText())
        self.device_ip.clear()
        Device[1] = (self.Fetch_sec.value())
        self.Fetch_sec.clear()
        Device[2] = (self.netconf_password.text())
        self.netconf_password.clear()
        Device[3] = (int(self.netconf_port.value()))
        self.netconf_port.clear()
        Device[4] = (self.netconf_admin.displayText())
        self.netconf_admin.clear()
        self.modify_json_network()
    #Include Notification changes in config.jason file
    def modify_json(self):
        try:
            import os
            filename = os.path.join(os.path.dirname(__file__), '../config/config.json')

            with open(filename, 'r') as json_file:
                data = json.load(json_file)
                try:
                    with open(filename, 'w') as json_file:

                        data['Notification_config']['Sender_email'] = Notification[0]
                        data['Notification_config']['Sender_email_password'] = Notification[1]
                        data['Notification_config']['Receiver_Email'] = Notification[2]
                        data['Notification_config']['Severity_notification_threshold'] = Notification[3]
                        data['Notification_config']['Send_email'] = Notification[4]
                        data['Notification_config']['Send_message'] = Notification[5]

                        json.dump(data, json_file, indent=4, sort_keys=True)

                        self.Run()
                except Exception as e:
                    logging.log(logging.CRITICAL, "Error writing config.json file! -> " + str(e))
        except Exception as e:
            logging.log(logging.CRITICAL, "Error reading config.json file! -> " + str(e))
    # Include Network changes in config.jason file
    def modify_json_network(self):
        try:
            import os
            filename = os.path.join(os.path.dirname(__file__), '../config/config.json')

            with open(filename, 'r') as json_file:
                data = json.load(json_file)
                try:
                    with open(filename, 'w') as json_file:
                        new_device ={
                            "device_ip": Device[0],
                            "netconf_fetch_rate_in_sec": Device[1],
                            "netconf_password": Device[2],
                            "netconf_port": Device[3],
                            "netconf_user": Device[4]
                        }
                        data['Network'].append(new_device)

                        json.dump(data, json_file, indent=4, sort_keys=True)
                except Exception as e:
                    logging.log(logging.CRITICAL, "Error writing config.json file! -> " + str(e))
        except Exception as e:
            logging.log(logging.CRITICAL, "Error reading config.json file! -> " + str(e))
    #Window in case information is not provided
    def json_changes_window(self,notif,ip):
        msg = QMessageBox()
        msg.setWindowTitle("Verify Configuration")
        msg.setWindowIcon(QtGui.QIcon(alarm_icon))
        msg.setText("Configurations where not selected:                                                                                 ")
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
                self.modify_json()
        msg.exec()
        if msg.clickedButton().text() == "Ignore":
            self.Run()

    # Verify if information was included
    def Verification_changes(self):
        notif=all(elem == Notification[0] for elem in Notification)
        ip=all(elem == Device[0] for elem in Device)
        if notif or ip:
            self.json_changes_window(notif,ip)
        else:
            self.modify_json()

    # Run Butoon is pressed
    def Run(self):
        # starting the Alarm Service
        t = threading.Thread(target=Main_Service)
        t.start()
        # Enable graphs and table
        self.formGroupBox.setEnabled(False)
        self.button_Notification.setEnabled(False)
        self.formGroupBox2.setEnabled(False)
        self.button_Device.setEnabled(False)
        self.button_RUN.setEnabled(False)
        self.load_db.setEnabled(True)
        self.tab_2.setEnabled(True)
        self.tab_3.setEnabled(True)
        self.tab_4.setEnabled(True)
        self.refreshButton.setEnabled(True)
    #Exit toolbar triggered
    def Exit(self):
        self.close()
    #Close event Warning
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Warning                                                                                                        ")
        msg.setWindowIcon(QtGui.QIcon(alarm_icon))
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setText("Are you sure you want to exit?")
        msg.setInformativeText("Press Yes for exit")
        msg.exec()
        if msg.clickedButton().text() == "&Yes":
            a0.accept()
        else:
            a0.ignore()
    #window with information about the app
    def About(self):
        msg = QMessageBox()
        msg.setWindowTitle("About                                                                                                        ")
        msg.setWindowIcon(QtGui.QIcon(alarm_icon))
        msg.setIcon(QMessageBox.Information)
        msg.setText("Authors:")
        version = config_manager.ConfigManager().get_version()
        msg.setInformativeText("Fabio Carminati\nEmanuele Gallone\nAndrés Rodríguez\n\n Version: " + version)
        msg.exec()
    #Save graphs methods
    def saveAllClicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Select the directory path where you want to store all the graphs")
        msg.setWindowIcon(QtGui.QIcon(floppy_icon))
        msg.setText("                                                                                                                               ")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Save)

        self.textbox = QLineEdit(msg)
        self.textbox.move(50, 20)
        self.textbox.resize(280,20)

        msg.exec()
        if msg.clickedButton().text() == "Save":
            directory = self.textbox.text()
            self.plotWidget1.saveGraph1(directory)
            self.plotWidget2.saveGraph2(directory)
            self.plotWidget3.saveGraph3(directory)

    def save1Clicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Select the directory path where you want to store graph 1")
        msg.setWindowIcon(QtGui.QIcon(floppy_icon))
        msg.setText("                                                                                                                               ")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Save)

        self.textbox = QLineEdit(msg)
        self.textbox.move(50, 20)
        self.textbox.resize(280,20)

        msg.exec()
        if msg.clickedButton().text() == "Save":
            directory = self.textbox.text()
            self.plotWidget1.saveGraph1(directory)

    def save2Clicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Select the directory path where you want to store graph 2")
        msg.setWindowIcon(QtGui.QIcon(floppy_icon))
        msg.setText(
            "                                                                                                                               ")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Save)

        self.textbox = QLineEdit(msg)
        self.textbox.move(50, 20)
        self.textbox.resize(280, 20)

        msg.exec()
        if msg.clickedButton().text() == "Save":
            directory = self.textbox.text()
            self.plotWidget2.saveGraph2(directory)

    def save3Clicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Select the directory path where you want to store graph 3")
        msg.setWindowIcon(QtGui.QIcon(floppy_icon))
        msg.setText(
            "                                                                                                                               ")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Save)

        self.textbox = QLineEdit(msg)
        self.textbox.move(50, 20)
        self.textbox.resize(280, 20)

        msg.exec()
        if msg.clickedButton().text() == "Save":
            directory = self.textbox.text()
            self.plotWidget3.saveGraph3(directory)
    #Main Window definition
    def setupUi(self, MainWindow):
        self.setObjectName("MainWindow")
        self.resize(1200, 650)
        self.setWindowIcon(QtGui.QIcon(alarm_icon))
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        #Toolbar Definitions
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1200, 650))
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
        #Title and subtitle of the main window
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(410, 10, 400, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(520, 50, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        #Defining and setting the table
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(420, 100, 720, 350))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        #Defining the Load Button
        self.load_db = QtWidgets.QPushButton(self.tab)
        self.load_db.setGeometry(QtCore.QRect(740, 465, 75, 23))
        self.load_db.setObjectName("load_db")
        self.load_db.setEnabled(False)
        # Defining the Notification Button
        self.button_Notification = QtWidgets.QPushButton(self.tab)
        self.button_Notification.setGeometry(QtCore.QRect(120, 270, 180, 20))
        self.button_Notification.setObjectName("button_Notification")
        #Defining the new Device Button
        self.button_Device = QtWidgets.QPushButton(self.tab)
        self.button_Device.setGeometry(QtCore.QRect(120, 465, 110, 20))
        self.button_Device.setObjectName("button_Device")
        #Defining the Run Button
        self.button_RUN = QtWidgets.QPushButton(self.tab)
        self.button_RUN.setGeometry(QtCore.QRect(550, 525, 110, 20))
        self.button_RUN.setObjectName("button_RUN")
        # Defining the Refresh Button
        self.refreshButton = QtWidgets.QPushButton(self.tab)
        self.refreshButton.setGeometry(QtCore.QRect(870, 525, 110, 25))
        self.refreshButton.setObjectName("button_refreash")
        self.refreshButton.setEnabled(False)
        #Defining the Notification Options Box
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
        self.formGroupBox.setGeometry(QtCore.QRect(20, 100, 300, 160))
        layout = QFormLayout()
        layout.addRow(QLabel("Sender_email:"), self.Send_Mail)
        layout.addRow(QLabel("Password:"), self.Password)
        layout.addRow(QLabel("Receiver_Email:"), self.Reciver_Mail)
        layout.addRow(QLabel("Severity Threshold:"), self.Severity)
        layout.addRow(QLabel("Send E-mail:"), self.Mail_Button)
        layout.addRow(QLabel("Send Message:"), self.Message_Button)
        self.formGroupBox.setLayout(layout)
        # Defining the Device Options Box
        self.device_ip = QLineEdit()
        self.Fetch_sec = QSpinBox()
        self.Fetch_sec.setMaximum(10)
        self.netconf_password = QLineEdit()
        self.netconf_password.setEchoMode(2)
        self.netconf_port = QSpinBox()
        self.netconf_port.setMaximum(1000)
        self.netconf_admin = QLineEdit()

        self.formGroupBox2 = QGroupBox(self.tab)
        self.formGroupBox2.setGeometry(QtCore.QRect(20, 300, 300, 150))
        layout2 = QFormLayout()
        layout2.addRow(QLabel("Device Ip:"), self.device_ip)
        layout2.addRow(QLabel("Netconf User:"), self.netconf_admin)
        layout2.addRow(QLabel("Netconf Password:"), self.netconf_password)
        layout2.addRow(QLabel("Netconf Port:"), self.netconf_port)
        layout2.addRow(QLabel("Fetch Rate:"), self.Fetch_sec)
        self.formGroupBox2.setLayout(layout2)
        #Triggered (Clicked) Buttons connections with respective methods
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()
        self.load_db.clicked.connect(self.loadDataB)

        self.button_Notification.clicked.connect(self.Json_Notification)
        self.button_Device.clicked.connect(self.Json_Network)
        self.button_RUN.clicked.connect(self.Verification_changes)
        self.refreshButton.clicked.connect(self.reFresh)
        #Defining Graphs
        self.plotWidget1 = Graph1(self.tab_2, width=12, height=4.5, dpi=100)
        self.plotWidget1.move(0, 100)
        self.plotWidget2 = Graph2(self.tab_3, width=12, height=5, dpi=100)
        self.plotWidget2.move(0, 80)
        self.plotWidget3 = Graph3(self.tab_4, width=12, height=4.5, dpi=100)
        self.plotWidget3.move(20, 100)

        self.setCentralWidget(self.centralwidget)
        #DEfining and setting the toolbar
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 918, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.actionExit = QtWidgets.QAction()
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setIcon(QtGui.QIcon(exit_icon))

        self.actionAbout = QtWidgets.QAction()
        self.actionAbout.setObjectName("actionAbout")

        self.actionAbout.triggered.connect(self.About)

        self.actionSaveAll = QtWidgets.QAction()
        self.actionSaveAll.setObjectName("actionSaveAll")
        self.actionSaveAll.setIcon(QtGui.QIcon(floppy_icon))

        self.actionSave1 = QtWidgets.QAction()
        self.actionSave1.setObjectName("actionSave1")
        self.actionSave1.setIcon(QtGui.QIcon(floppy_icon))

        self.actionSave2 = QtWidgets.QAction()
        self.actionSave2.setObjectName("actionSave2")
        self.actionSave2.setIcon(QtGui.QIcon(floppy_icon))

        self.actionSave3 = QtWidgets.QAction()
        self.actionSave3.setObjectName("actionSave3")
        self.actionSave3.setIcon(QtGui.QIcon(floppy_icon))
        #Toolbar buttons connections
        self.actionExit.triggered.connect(self.Exit)
        self.actionSaveAll.triggered.connect(self.saveAllClicked)
        self.actionSave1.triggered.connect(self.save1Clicked)
        self.actionSave2.triggered.connect(self.save2Clicked)
        self.actionSave3.triggered.connect(self.save3Clicked)

        self.menuFile.addAction(self.actionSaveAll)
        self.menuFile.addAction(self.actionSave1)
        self.menuFile.addAction(self.actionSave2)
        self.menuFile.addAction(self.actionSave3)

        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(self)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
    #Visual names for the widgets
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Alarm Management Tool"))
        self.label.setText(_translate("MainWindow", "Smart Networks and Service Orchestration"))
        self.label_2.setText(_translate("MainWindow", "Alarm Management"))
        self.load_db.setText(_translate("MainWindow", "Load Table"))
        self.button_Notification.setText(_translate("MainWindow", "Edit notification parameters"))
        self.button_Device.setText(_translate("MainWindow", "Insert Device"))
        self.button_RUN.setText(_translate("MainWindow", "Run"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh ALL graphs"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Home"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Graph 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Graph 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Graph 3"))

        self.menuFile.setTitle(_translate("MainWindow", "File      "))
        self.menuAbout.setTitle(_translate("MainWindow", "?        "))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSaveAll.setText(_translate("MainWindow", "Save all Graphs"))
        self.actionSave1.setText(_translate("MainWindow", "Save Graph 1"))
        self.actionSave2.setText(_translate("MainWindow", "Save Graph 2"))
        self.actionSave3.setText(_translate("MainWindow", "Save Graph 3"))


def __main():
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # set stylesheet
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    _MainWindow = MainWindow()
    _MainWindow.show()
    sys.exit(app.exec_())


def gui_thread():
    import threading
    t = threading.Thread(target=__main)
    # t.daemon = True
    return t


if __name__ == '__main__':
    __main()
