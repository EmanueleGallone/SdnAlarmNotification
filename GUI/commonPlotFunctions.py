"""
Author Fabio Carminati , 05-2020

This class contains methods that are common amid the graph classes

"""
from models.database_manager import DBHandler
from models.config_manager import ConfigManager
from collections import defaultdict
import logging
import os

logfile = os.path.join(os.path.dirname(__file__), '../log.log')
logging.basicConfig(filename=logfile, level=logging.ERROR)

class CommonFunctions(object):
    def fetchDataFromDB(self):
        alarmTable = DBHandler()
        alarmTable.open_connection()
        results = alarmTable.select_all()
        alarmTable.close_connection()
        return results

    def organizeAlarmsPerHost(self,results):
        alarmsPerHost=defaultdict(lambda: defaultdict(int))

        for row in results:
            alarmsPerHost[row[1]][row[2]] += 1

        config_manager = ConfigManager()
        severity_levels = config_manager.get_severity_levels()

        for key, item in severity_levels.items():
            for host in alarmsPerHost:
                if str(item) not in alarmsPerHost[host]:
                    alarmsPerHost[host][str(item)] = 0
        return alarmsPerHost

    def organizeTotalAlarmsPerSeverity(self,results):
        totalAlarmsPerSeverity = defaultdict(int)
        for row in results:
            totalAlarmsPerSeverity[int(row[2])] += 1

        config_manager = ConfigManager()
        severity_levels = config_manager.get_severity_levels()

        for key, item in severity_levels.items():
            if item not in totalAlarmsPerSeverity:
                totalAlarmsPerSeverity[item] = 0
        return totalAlarmsPerSeverity

    # Given the severity index it returns its description
    def getInfo(self, element):
        _config_manager = ConfigManager()
        description=_config_manager.get_severity_mapping(element)
        return description

    # Save in the specified path the graph
    def saveSingleGraph(self, path,fig,graphID):
        try:
            fig.savefig(path)
        except Exception as e:
            logging.log(logging.CRITICAL, str(e) + ": we cannot save the graph "+str(graphID))

    #Attach a text label above each bar in *rects*, displaying its height
    def autolabel(self, rects, axes):
        for rect in rects:
            height = rect.get_height()
            axes.annotate('{}'.format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')