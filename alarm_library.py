"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

a bunch of useful methods retrieving alarms from SDN devices
"""

import threading, time, traceback, logging

import database_handler
from config_manager import ConfigManager


from ncclient import manager
from io import BytesIO
from typing import List
import lxml.etree as ET

####################setting up globals###################

logging.basicConfig(filename="log.log", level=logging.ERROR)

device_port = 830
db = database_handler.DBHandler()  # setting up the db connection

config_m = ConfigManager()

netconf_fetch_rate = config_m.get_netconf_fetch_rate()
devices = config_m.get_all_devices_ip()
netconf_port = config_m.get_netconf_port()
netconf_user = config_m.get_netconf_user()
netconf_password = config_m.get_netconf_password()

lock = threading.Lock()

#########################################


def worker(_delay, task, *args):
    """worker definition for thread task

    @param _delay: it specifies the delay in which the task will be performed
    @param task: pointer to the function that will be executed by the thread
    @param args: list of arguments that will be passed to the task's parameters
    @return: void
    """
    next_time = time.time() + _delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        logging.info("inside thread")
        try:
            task(*args)
        except Exception:
            traceback.print_exc()

            logging.exception("Problem while trying to retrieve alarms' data.")
            # skip tasks if we are behind schedule: todo: refactor using schedule library
        next_time += (time.time() - next_time) // _delay * _delay + _delay


def dummy_data_fetch() -> str:
    string_result = ''
    with open('dummy_data.txt', 'r') as file:
        for line in file:
            # if "<?xml " in line:  # remove the xml prolog
            #     continue

            string_result += (line.rstrip())

    return string_result


def repeated_get_alarms(host, port, user, password):
    result = parse_to_ElementTree(dummy_data_fetch())

    for element in result.iter("*"):
        if element.text is not None:
            lock.acquire()
            print(element.tag, element.text)
            lock.release()


def parse_to_ElementTree(xml='') -> ET:

    xml_string = BytesIO(bytes(xml, encoding='utf-8'))

    return ET.parse(xml_string)


def get_alarms_xml(host, port, user, password) -> str:
    with manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=10,
                           hostkey_verify=False) as conn:

        criteria = """
        <managed-element xmlns="http://www.advaoptical.com/aos/netconf/aos-core-managed-element">
            <alm-summary />
        </managed-element>
        """

        criteria2 = """
        <managed-element xmlns="http://www.advaoptical.com/aos/netconf/aos-core-managed-element"> <entity-name>1</entity-name> <interface xmlns="http://www.advaoptical.com/aos/netconf/aos-core-facility"> <name>1/1/ot100</name> <floating-interface/> </interface> </managed-element>
        """

        filter = ("subtree", criteria)
        result = conn.get(filter)

    return result


def start_threads() -> List:

    threads = []
    for device in devices:
        t = threading.Thread(target=lambda: worker(netconf_fetch_rate, repeated_get_alarms, device, netconf_port, netconf_user, netconf_password))
        threads.append(t)

    for t in threads:  # starting all the threads
        t.start()

    return threads


if __name__ == "__main__":
    # url = 'http://10.11.12.16:7777/restconf/data/tapi-common:context'
    # print(get_request(url))

    #result = get_alarms_xml('10.11.12.19', 830, 'admin', 'CHGME.1a').data_xml
    #print(result)

    threads = start_threads()

    for thread in threads:
        thread.join()

    root = parse_to_ElementTree()

    for element in root.iter("*"):
        if element.text is not None:
            print(element.tag, element.text)


