from models.database_handler import DBHandler
from models.config_manager import ConfigManager
from collections import defaultdict
import logging
import os
dirname = os.path.dirname(__file__)

logging.basicConfig(filename="../../log.log", level=logging.ERROR)

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

    def getInfo(self, element):
        _config_manager = ConfigManager()
        description=_config_manager.get_severity_mapping(element)
        return description