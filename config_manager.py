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

# todo: refactor in a way that your read the file only once!


def _read_config_file() -> Dict:  # creating static method to read config file
    try:
        data = {}
        with open('config.json', 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        logging.log(logging.CRITICAL, "Error reading config.json file! -> " + str(e))
    finally:
        return data


class ConfigManager:
    def __init__(self):
        self.data = ''

    def read_network_params(self) -> Dict:

        self.data = _read_config_file()['network_params']
        return self.data

    def get_notification_params(self) -> Dict:
        self.data = _read_config_file()['notification_config']
        return self.data

    def get_all_devices_ip(self) -> List:
        self.data = _read_config_file()['network_params']['devices_ip']
        return self.data

    def get_netconf_port(self) -> List:
        self.data = _read_config_file()['network_params']['netconf_port']
        return self.data

    def get_netconf_user(self) -> str:
        self.data = _read_config_file()['network_params']['netconf_credentials']['user']
        return self.data

    def get_netconf_password(self) -> str:
        self.data = _read_config_file()['network_params']['netconf_credentials']['password']
        return self.data

    def get_netconf_fetch_rate(self) -> str:
        self.data = _read_config_file()['network_params']['netconf_fetch_rate_in_sec']
        return self.data

    def get_debug_mode(self) -> str:
        self.data = _read_config_file()['Debug_Mode']
        return self.data


if __name__ == '__main__':
    # debug
    c = ConfigManager()

    print(c.read_network_params())
    print(c.get_notification_params())
    print(c.get_all_devices_ip()[0])
    print(c.get_netconf_user() , c.get_netconf_password())
    print(c.get_debug_mode())
