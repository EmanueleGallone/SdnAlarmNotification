from models.database_handler import DBHandler
import logging
class CommonFunctions(object):
    def fetchDataFromDB(self):
        alarmTable = DBHandler()
        alarmTable.open_connection()
        results = alarmTable.select_all()
        alarmTable.close_connection()
        return results
