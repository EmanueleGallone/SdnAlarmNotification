"""
Author Emanuele Gallone

Wrapper class to implement a custom XML parser.
The only method exposed to the outside is parse_all_alarms_xml()
"""
from io import BytesIO
from typing import List

import lxml.etree as ET
import lxml.objectify as objectify


class CustomXMLParser(object):

    def __init__(self, xml):
        self.xml = xml
        self.root = None

    def __remove_namespaces(self) -> ET:
        """
        It does exactly what the method's name specifies.
        For the love of god, don't touch this. It was a nightmare finding how to do this
        inside the documentation.

        it could be useless, just ignore namespaces using lxml. maybe a refactor will be needed.

        @return: lxml.ElementTree object
        """

        for _elem in self.root.getiterator():
            if not hasattr(_elem.tag, 'find'):
                continue
            _i = _elem.tag.find('}')
            if _i >= 0:
                _elem.tag = _elem.tag[_i + 1:]
        objectify.deannotate(self.root, cleanup_namespaces=True)

        return self

    def __parse_to_ElementTree(self):
        """
        creates a lxml.ElementTree from a xml in string format
        @param xml: xml in string format
        @return: lxml.ElementTree object
        """
        xml_string = BytesIO(bytes(self.xml, encoding='utf-8'))
        self.root = ET.parse(xml_string).getroot()

        return self.__remove_namespaces()

    def parse_all_alarms_xml(self) -> List:
        """
        method that parse and filters all the xml inside the lxml.ElementTree that we're interested in

        @return: List of Dictionaries containing alarms metadata [{alarm_ID: {element.tag: element.text}}]
        """
    # todo refactor this immediately. it's unreadable. use list comprehension
        self.__parse_to_ElementTree()

        _data = []
        _tags_interested_in = ['condition-description', 'ne-condition-timestamp', 'notification-code']

        for alarm in self.root.findall('*/managed-element/'):
            my_dict = {}

            for child in alarm:
                if child.tag in _tags_interested_in:

                    if child.tag == _tags_interested_in[2]:  # (notification-code) replacing useless namespace
                        child.text = str(child.text).replace('acor-fmt:', '')

                    if child.tag == _tags_interested_in[1]:  # (timestamp) formatting the datetime
                        child.text = str(child.text).replace('T', ' ')
                        child.text = str(child.text).replace('Z', '')

                    # all the tags that don't need editing go directly inside the dictionary (e.g. condition-description)
                    my_dict[child.tag] = child.text

            _data.append(my_dict)

        return _data


if __name__ == '__main__':
    from alarm_library import _detail_dummy_data_fetch
    c = CustomXMLParser(_detail_dummy_data_fetch()).parse_all_alarms_xml()
    print(c)

