"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

a bunch of useful methods retrieving alarms from SDN devices using NETCONF
"""

import threading, time, traceback, logging

import database_handler
from config_manager import ConfigManager


from ncclient import manager
from io import BytesIO
from typing import List
from lxml import etree as ET, objectify

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


def _worker(_delay, task, *args):
    '''
    worker definition for thread task

    @param _delay: it specifies the delay in which the task will be performed
    @param task: pointer to the function that will be executed by the thread
    @param args: list of arguments that will be passed to the task's parameters
    @return: void
    '''
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


def _dummy_data_fetch() -> str:
    string_result = ''
    with open('dummy_data.txt', 'r') as file:
        for line in file:
            # if "<?xml " in line:  # remove the xml prolog
            #     continue

            string_result += (line.rstrip())

    return string_result


def repeated_get_alarms(host, port, user, password):

    # change to get_alarms to really fetch data from SDN devices
    try:
        temp = get_alarms_xml(host, port, user, password)
    except Exception as e:
        logging.log(logging.ERROR, "Could not retrieve data from netconf! switching to dummy data\n" + str(e))
        temp = _dummy_data_fetch()

    result = _parse_to_ElementTree(temp)

    # result = parse_to_ElementTree(_dummy_data_fetch())

    for element in result.iter("*"):
        if element.text is not None:
            lock.acquire()
            print(element.tag, element.text)
            lock.release()


def __remove_namespaces(_root):
    '''
    It does exactly what the name's specifies
    @param _root: root of xml tree lxml.ElementTree format
    '''

    for _elem in _root.getiterator():
        if not hasattr(_elem.tag, 'find'):
            continue
        _i = _elem.tag.find('}')
        if _i >= 0:
            _elem.tag = _elem.tag[_i + 1:]
    objectify.deannotate(_root, cleanup_namespaces=True)

    return _root


def _parse_severity(root) -> List:
    alarms = []

    if root is None:
        raise Exception("Root not set!")

    # I'm lazy, I don't know how to reach the tags using XPATH
    # (potentially O(n) -> not good)
    for element in root.iter("*"):
        if element.text is not None:
            try:
                severity = {  # ideally it works as a switch-case (not present in python, of course...)
                    'critical-alm-count': 5,
                    'major-alm-count': 4,
                    'minor-alm-count': 3,
                    'warn-alm-count': 2,
                    'na-alm-count': 1,
                    'nr-alm-count': 0
                }[element.tag]
            except KeyError as k:
                severity = -1

            if severity != -1:
                quantity = element.text  # the element text shows the number of alarms
                alarms.append((severity, quantity))

    return alarms


def _parse_to_ElementTree(xml='') -> ET:

    xml_string = BytesIO(bytes(xml, encoding='utf-8'))
    tree = ET.parse(xml_string)
    _root = tree.getroot()

    return __remove_namespaces(_root)


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
        result = conn.get(filter).xml

    return result


def start_threads() -> List:

    _threads = []

    for device in devices:
        _t = threading.Thread(target=lambda: _worker(netconf_fetch_rate, repeated_get_alarms, device, netconf_port, netconf_user, netconf_password))
        _t.start()
        _threads.append(_t)

    return _threads


if __name__ == "__main__":
    # url = 'http://10.11.12.16:7777/restconf/data/tapi-common:context'
    # print(get_request(url))

    threads = start_threads()

    for thread in threads:
        thread.join()

    root = _parse_to_ElementTree(_dummy_data_fetch())

    _parse_severity(root)
