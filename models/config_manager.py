"""
Author Emanuele Gallone, 05-2020

Simple wrapper class to decouple the reading of the config.json file
from the rest of the program.

"""

import json
import logging
import os
import time
from typing import Dict, List

dirname = os.path.dirname(__file__)

logfile = os.path.join(dirname, '../log.log')
logging.basicConfig(filename=logfile, level=logging.ERROR)


def _read_config_file() -> Dict:  # creating static method to read config file
    filename = os.path.join(dirname, '../config/config.json')

    try:
        data = {}
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        logging.log(logging.CRITICAL, "Error reading config/config.json file! -> " + str(e))

    finally:
        return data


class ConfigManager(object):
    def __init__(self):
        self.data = _read_config_file()

    def get_network_params(self) -> List:
        return self.data['Network']

    def get_notification_config(self) -> Dict:
        return self.data['Notification_config']

    def get_email_notification_flag(self) -> bool:
        return self.get_notification_config()['Send_email']

    def get_message_notification_flag(self) -> bool:
        return self.get_notification_config()['Send_message']

    def get_debug_mode(self) -> bool:
        return  self.data['Debug_Mode']

    def get_severity_levels(self) -> Dict:
        return self.data['Severity_levels']

    def get_severity_notification_threshold(self) -> int:
        return self.get_notification_config()['Severity_notification_threshold']

    def get_alarm_dummy_data_flag(self) -> bool:
        return self.data['Do_not_save_existing_alarms']

    def get_version(self) -> str:
        return self.data['Version']

    def getSeveritiesNumber(self) -> int:
        return len(self.data['Severity_levels'])

    def get_severity_mapping(self, severity) -> str:
        """
        returns the dict mapping of severity levels (see in config.json)
        @param severity: must be a int
        """
        if severity is not None:
            levels = self.data['Severity_levels']
            result = ''
            try:
                result = [k for k, v in levels.items() if v == severity][0]
            except Exception as e:
                logging.log(logging.ERROR, 'Cannot find Severity in mapping!' + str(e) + 'severity : ' + str(severity))
            finally:
                return result


if __name__ == '__main__':
    # debug
    c = ConfigManager()

    print(c.get_network_params())
    print(c.get_notification_config())
    print(c.get_debug_mode(),
          c.get_alarm_dummy_data_flag(),
          c.get_email_notification_flag(),
          c.get_message_notification_flag(),
          )

    time.sleep(10)
    print(c.get_severity_mapping(6))
    print(c.get_version())
