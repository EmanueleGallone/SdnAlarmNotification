"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

This class is responsible for notifying the user about alarms. It uses a singleton architecture
"""
import logging
import threading
import time
import traceback

from models.database_handler import DBHandler
from services import telegram_bot_service, mail_sender_service
from models.config_manager import ConfigManager

logging.basicConfig(filename="../log.log", level=logging.ERROR)


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

    def notify(self, msg="DEBUG FROM NOTIFICATION MANAGER!"):
        self._send_mail(msg)
        self._broadcast_alarm(msg)

    def _send_mail(self, msg):
        send_email_flag = self._config_manager.get_email_notification_flag()

        if send_email_flag:
            mail_sender_service.send_mail(msg)

    def _broadcast_alarm(self, msg):
        send_message_flag = self._config_manager.get_message_notification_flag()

        if send_message_flag:
            telegram_bot_service.send_to_bot_group(msg)

    def start(self):

        notifier = threading.Thread(target=lambda: self.__notificationThread(5))
        notifier.start()

        return notifier

    def __build_new_alarm_msg(self, _list) -> str:

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

        ids = []
        for alarm in _list:
            ids.append(alarm[0])

        db = DBHandler().open_connection()
        db.update_notified_by_ID(ids)
        db.close_connection()

    def __notificationThread(self, _delay):

        """
        worker definition for thread task

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
