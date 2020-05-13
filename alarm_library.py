"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

a bunch of useful methods retrieving alarms from SDN devices using NETCONF.

"""

import threading, time, traceback, logging

from database_handler import DBHandler
from config_manager import ConfigManager

from ncclient import manager
from io import BytesIO
from typing import List
from lxml import etree as ET, objectify

####################setting up globals###################

logging.basicConfig(filename="log.log", level=logging.ERROR)

device_port = 830

config_m = ConfigManager()

netconf_fetch_rate = config_m.get_netconf_fetch_rate()
devices = config_m.get_all_devices_ip()
netconf_port = config_m.get_netconf_port()
netconf_user = config_m.get_netconf_user()
netconf_password = config_m.get_netconf_password()

lock = threading.Lock()


#########################################


def _worker(_delay, task, *args):
    # todo specify thread's stop condition?
    """
    worker definition for thread task

    @param _delay: it specifies the delay in which the task will be performed
    @param task: pointer to the function that will be executed by the thread
    @param args: list of arguments that will be passed to the task's parameters
    @return: void
    """
    next_time = time.time() + _delay
    while True:
        time.sleep(max(0, next_time - time.time()))  # making the threads not wasting CPU cycles

        try:
            task(*args)
        except Exception:
            traceback.print_exc()

            logging.exception("Problem while trying to retrieve alarms' data.")
            # skip tasks if we are behind schedule: todo: refactor using schedule library
        next_time += (time.time() - next_time) // _delay * _delay + _delay


def _detail_dummy_data_fetch() -> str:
    """
    I created this method to have a dummy data in case a device goes down or VPN isn't working
    NB: for testing purpose only!!!
    @return: xml in string format
    """
    string_result = ''
    with open('detail_dummy_data.xml', 'r') as _file:
        for _line in _file:
            # if "<?xml " in line:  # remove the xml prolog
            #     continue

            string_result += (_line.rstrip())

    return string_result


def _thread_get_alarms(host, port, user, password):
    """
    this method is ran by the various threads. It is the core concept of the alarm library
    @param host: device IP
    @param port: netconf port
    @param user: username credential for netconf
    @param password: password for netconf
    @return: void
    """
    try:
        temp = _get_alarms_xml(host, port, user, password)

    except Exception as e:

        logging.log(logging.ERROR, "Could not retrieve data from netconf! switching to dummy data\n" + str(e))
        temp = _detail_dummy_data_fetch()

    _root = _parse_to_ElementTree(temp)  # first, let's convert the xml to ElementTree object

    alarms_metadata = _parse_all_alarms_xml(_root)  # then we parse the xml to retrieve all the metadata that we need

    _thread_save_to_db(host, alarms_metadata)  # finally save the information in DB

    return


def _thread_save_to_db(host, parsed_metadata):
    """
    method used by the various threads to save inside the local.db all the metadata that we need
    here the things gets a little tricky:
    basically, parsed_metadata is a list of dictionaries. Each dictionary is an alarm.
    If you want to know how this dictionary is built look at _parse_all_alarms_xml(_root)

    @param host: specifies the host IP
    @param parsed_metadata: is a list of dictionaries that is coming from the method '_parse_all_alarms_xml(_root)'
    @return: void
    """

    for alarm_dict in parsed_metadata:

        severity_levels = config_m.get_severity_levels()
        severity = severity_levels[alarm_dict['notification-code']]
        description = alarm_dict['condition-description']
        timestamp = alarm_dict['ne-condition-timestamp']

        lock.acquire()
        db_handler = DBHandler()

        db_handler.open_connection()

        # todo verify if alarm already inserted
        db_handler.insert_row_alarm(device_ip=host,
                                    severity=severity,
                                    description=description,
                                    _time=timestamp,
                                    notified=0)
        db_handler.close_connection()

        lock.release()


def __remove_namespaces(_root) -> ET:
    """
    It does exactly what the method's name specifies.
    For the love of god, don't touch this. It was a nightmare finding how to do this
    inside the documentation.

    @param _root: root of xml tree lxml.ElementTree format
    @return: lxml.ElementTree object
    """

    for _elem in _root.getiterator():
        if not hasattr(_elem.tag, 'find'):
            continue
        _i = _elem.tag.find('}')
        if _i >= 0:
            _elem.tag = _elem.tag[_i + 1:]
    objectify.deannotate(_root, cleanup_namespaces=True)

    return _root


def _parse_to_ElementTree(xml='') -> ET:
    """
    creates a lxml.ElementTree from a xml in string format
    @param xml: xml in string format
    @return: lxml.ElementTree object
    """
    xml_string = BytesIO(bytes(xml, encoding='utf-8'))
    tree = ET.parse(xml_string)
    _root = tree.getroot()

    return __remove_namespaces(_root)


def _get_alarms_xml(host, port, user, password) -> str:
    """
    method that connect to the specified host,port using the credentials specified in user,password to retrieve
    alarm information
    @param host: Device IP
    @param port: Device's netconf port
    @param user: Device's netconf user credential
    @param password: Device's netconf password credential
    @return: xml from netconf, as a string
    """
    with manager.connect(host=host,
                         port=port,
                         username=user,
                         password=password,
                         timeout=10,
                         hostkey_verify=False) as conn:

        retrieve_all_alarms_criteria = """
        <managed-element xmlns:acor-me="http://www.advaoptical.com/aos/netconf/aos-core-managed-element"> 
        <alarm/> </managed-element>
        """

        filter = ("subtree", retrieve_all_alarms_criteria)
        result = conn.get(filter).xml

    return result


def _parse_all_alarms_xml(_root) -> List:
    """
    method that parse and filters all the xml inside the lxml.ElementTree that we're interested in

    @param _root: is the lxml.ElementTree containing the xml we need to parse
    @return: List of Dictionaries containing alarms metadata [{alarm_ID: {element.tag: element.text}}]
    """
    # todo refactor this immediately. it's unreadable

    data = []
    tags_interested_in = ['condition-description', 'ne-condition-timestamp', 'notification-code']

    for alarm in _root.findall('*/managed-element/'):
        my_dict = {}

        for child in alarm:
            if child.tag in tags_interested_in:

                if child.tag == tags_interested_in[2]:  # (notification-code) replacing useless namespace
                    child.text = str(child.text).replace('acor-fmt:', '')

                if child.tag == tags_interested_in[1]:  # (timestamp) formatting the datetime
                    child.text = str(child.text).replace('T', ' ')
                    child.text = str(child.text).replace('Z', '')

                # all the tags that don't need editing go directly inside the dictionary (e.g. condition-description)
                my_dict[child.tag] = child.text

        data.append(my_dict)

    return data


def start_threads() -> List:
    """
    method available on the outside. it start all the magic to retrive the alarms on the devices
    listed inside the config.json

    @return: List of threads that need to be joined outside
    """
    _threads = []

    for device in devices:
        _t = threading.Thread(
            target=lambda: _worker(netconf_fetch_rate, _thread_get_alarms, device, netconf_port, netconf_user,
                                   netconf_password))
        _t.start()
        _threads.append(_t)

    return _threads


if __name__ == "__main__":

    threads = start_threads()

    for thread in threads:
        thread.join()

    result = ''
    with open('detail_dummy_data.xml', 'r') as file:
        for line in file:
            result += line.rstrip()

    print(result)
    root = _parse_to_ElementTree(result)
