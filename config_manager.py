"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

Simple wrapper class to decouple the reading of the config.json file
from the rest of the program
"""

import json
import logging
from typing import Dict, List

logging.basicConfig(filename="log.log", level=logging.ERROR)

# todo refactor in a way to read the file only once!

def _read_config_file() -> Dict:  # creating static method to read config file
    try:
        data = {}
        with open('config.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        logging.log(logging.CRITICAL, "Error reading config.json file! -> " + str(e))
    finally:
        return data


class ConfigManager(object):
    def __init__(self):
        self.data = _read_config_file()

    def read_network_params(self) -> Dict:
        return self.data['network_params']

    def get_notification_params(self) -> Dict:
        return self.data['notification_config']

    def get_all_devices_ip(self) -> List:
        return self.data['network_params']['devices_ip']

    def get_netconf_port(self) -> List:
        return self.data['network_params']['netconf_port']

    def get_netconf_user(self) -> str:
        return self.data['network_params']['netconf_credentials']['user']

    def get_netconf_password(self) -> str:
        return self.data['network_params']['netconf_credentials']['password']

    def get_netconf_fetch_rate(self) -> str:
        return self.data['network_params']['netconf_fetch_rate_in_sec']

    def get_debug_mode(self) -> str:
        return self.data['Debug_Mode']

    def get_severity_levels(self) -> Dict:
        return self.data['Severity_levels']

    def get_severity_notification_threshold(self) -> int:
        return self.data['Severity_notification_threshold']


if __name__ == '__main__':
    # debug
    c = ConfigManager()

    print(c.read_network_params())
    print(c.get_notification_params())
    print(c.get_all_devices_ip()[0])
    print(c.get_netconf_user() , c.get_netconf_password())
    print(c.get_debug_mode())
    print(c.get_severity_levels())
