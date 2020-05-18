import logging
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
import sys
from models.database_handler import DBHandler
from models.config_manager import ConfigManager
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import random
dirname = os.path.dirname(__file__)
import numpy as np
import sqlite3


logging.basicConfig(filename="../../log.log", level=logging.ERROR)
class Plot2(FigureCanvas):
    def __init__(self, parent=None, width=7, height=5, dpi=100,updateCheck=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        #self.fig.tight_layout()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.updateCheck=updateCheck
        self.barGraph(self.axes)

    def barGraph(self,axes):
        print("here")
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

                        if self.updateCheck == True:
                            means.append(data[0]+random.randint(3,10))
                        else:
                            means.append(data[0])

                rects.append(means)

            #print(alarms_description)
            #print(rects)

            x = np.arange(len(labels))  # the label locations
            width = 0.2  # the width of the bars
            i=0
            for i in range(0, len(rects)):

                bar= axes.bar(x + (i-(len(rects)-1)/2) * width / 2, rects[i], width/2, label=list(alarms_description)[i])
                self.autolabel(bar,axes)
                #print(rects[i])
            # Add some text for labels, title and custom x-axis tick labels, etc.
            axes.set_ylabel('Number of Alarms')
            axes.set_title('Alarms by IP')
            axes.set_xticks(x)
            axes.set_xticklabels(labels)
            axes.legend(bbox_to_anchor= (0,-0.5),loc='lower left')
            connection.close()
            plt.show()
        except Exception as e:
            logging.log(logging.ERROR, "something wrong opening the Data Base" + str(e))

    def reStartPlot2(self):
        self.barGraph(self.axes)


    def autolabel(self, rects, axes):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            axes.annotate('{}'.format(height),
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, 3),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom')

