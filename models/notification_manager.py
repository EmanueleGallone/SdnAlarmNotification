"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

This class is responsible for notifying the user about alarms. It uses a singleton architecture.
I created this class to decouple the notification handling from the rest of the application.
If you want to add new notification methods (e.g. sending SMS) simply create a private method
and call it inside the notify() method.
"""
import logging
import threading
import time
import traceback
import os

from models.database_manager import DBHandler
from models.config_manager import ConfigManager
from services import mail_sender_service


logfile = os.path.join(os.path.dirname(__file__), '../log.log')
logging.basicConfig(filename=logfile, level=logging.WARNING)

try:
    from services import mysterious_service
except ImportError as e:
    logging.log(logging.WARNING, 'Could not find the telegram bot' + str(e))


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NotificationManager(object, metaclass=Singleton):

    def __init__(self):
        self._config_manager = ConfigManager()
        self.msg = ''
        self._worker = None

    def notify(self, msg="DEBUG FROM NOTIFICATION MANAGER!"):
        """ method that broadcast the alarm through all the technologies defined here (eg. email, messages...)"""
        self._send_mail(msg)
        self._broadcast_alarm(msg)

    def _send_mail(self, msg):
        """ helper method that sends the email through the service if the flag inside config.json is set to true"""
        send_email_flag = self._config_manager.get_email_notification_flag()

        if send_email_flag:
            mail_sender_service.send_mail(msg)

    def _broadcast_alarm(self, msg):
        """ broadcast the alarm using the bot"""
        send_message_flag = self._config_manager.get_message_notification_flag()

        try:
            if send_message_flag:
                mysterious_service.send_to_bot_group(msg)

        except Exception as e:
            logging.log(logging.ERROR, 'Failed to send a broadcast message' + str(e))

    def start(self):
        """method available on the outside. It just starts the thread responsible to deliver notifications to users."""
        # TODO make the delay of notification available on the config.json
        if self._worker is None:
            self._worker = threading.Thread(target=lambda: self.__notificationThread(5))
            self._worker.start()

        return self._worker

    def __build_new_alarm_msg(self, _list) -> str:
        """
        helper method that build the msg to be notified

        @param _list: list of dictionaries. each dictionary is an alarm
        @return a message formatted with all the information
        """

        self.message = 'New Alarm(s): \n'

        for alarm in _list:
            device = alarm[1]
            severity = alarm[2]
            description = alarm[3]
            timestamp = alarm[4]

            self.message += f'\tDeviceIp: \'{device}\',\n' \
                            f'\tDescription: {description},\n' \
                            f'\ttime: \'{timestamp}\'.\n' \
                            f'\tSeverity: {severity}\n\n'

        return self.message

    def __update_alarms_table_notified(self, _list):
        """
        method used to update the DB's table. It sets the notified attribute to 1 to all
        the alarms that were notified.
        @param _list: list of alarms
        """

        ids = []
        for alarm in _list:
            ids.append(alarm[0])

        db = DBHandler().open_connection()
        db.update_notified_by_ID(ids)
        db.close_connection()

    def __notificationThread(self, _delay):

        """
        worker definition for notification task. It queries the DB and chooses what alarms to notify.

        @param _delay: it specifies the delay in which the task will be performed
        @return: void
        """
        next_time = time.time() + _delay

        severity_threshold = self._config_manager.get_severity_notification_threshold()

        while True:
            time.sleep(max(0, next_time - time.time()))  # making the thread not wasting CPU cycles
            db = DBHandler()

            try:
                db.open_connection()

                result = db.select_alarm_by_severity_unnotified(severity_threshold)

                if len(result) != 0:  # it means that there are some alarms that need to be notified!
                    self.notify(self.__build_new_alarm_msg(result))
                    self.__update_alarms_table_notified(result)

            except Exception as e:
                traceback.print_exc()
                logging.exception("Problem while trying notify alarms' data." + str(e))

            finally:
                db.close_connection()

            next_time += (time.time() - next_time) // _delay * _delay + _delay  # next scheduling


if __name__ == '__main__':
    # DEBUG
    notification_m = NotificationManager().start()

    notification_m.join()
