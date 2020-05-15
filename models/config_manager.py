"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

Simple wrapper class to decouple the reading of the config.json file
from the rest of the program

NB: inside the config.json the bool are of string type, because json bool is 'true'
but python's bool is 'True'; this was the simplest workaround.
"""

import json
import logging
from typing import Dict, List

logging.basicConfig(filename="../log.log", level=logging.ERROR)


def _read_config_file() -> Dict:  # creating static method to read config file
    try:
        data = {}
        with open('config/config.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        logging.log(logging.CRITICAL, "Error reading config.json file! -> " + str(e))
    finally:
        return data


class ConfigManager(object):
    def __init__(self):
        self.data = _read_config_file()

    def get_network_params(self) -> Dict:
        return self.data['Network_params']

    def get_notification_config(self) -> Dict:
        return self.data['Notification_config']

    def get_email_notification_flag(self) -> bool:
        return True if self.get_notification_config()['Send_email'] == 'True' else False

    def get_message_notification_flag(self) -> bool:
        return True if self.get_notification_config()['Send_message'] == 'True' else False

    def get_all_devices_ip(self) -> List:
        return self.get_network_params()['devices_ip']

    def get_netconf_port(self) -> List:
        return self.get_network_params()['netconf_port']

    def get_netconf_user(self) -> str:
        return self.get_network_params()['netconf_credentials']['user']

    def get_netconf_password(self) -> str:
        return self.get_network_params()['netconf_credentials']['password']

    def get_netconf_fetch_rate(self) -> str:
        return self.get_network_params()['netconf_fetch_rate_in_sec']

    def get_debug_mode(self) -> bool:
        return True if self.data['Debug_Mode'] == "True" else False

    def get_severity_levels(self) -> Dict:
        return self.data['Severity_levels']

    def get_severity_notification_threshold(self) -> int:
        return self.get_notification_config()['Severity_notification_threshold']

    def get_alarm_dummy_data_flag(self) -> bool:
        return True if self.data['Do_not_save_existing_alarms'] == "True" else False


if __name__ == '__main__':
    # debug
    c = ConfigManager()

    print(c.get_network_params())
    print(c.get_notification_config())
    print(c.get_all_devices_ip()[0])
    print(c.get_netconf_user() , c.get_netconf_password())
    print(c.get_debug_mode())
    print(c.get_severity_levels())
