import alarm_library

from models.notification_manager import NotificationManager
from models.database_handler import DBHandler
from services import telegram_bot_service
from models.config_manager import ConfigManager

import threading
import time
import traceback
import logging

logging.basicConfig(filename="../log.log", level=logging.ERROR)

# todo refactor


def _build_new_alarm_msg(_list) -> str:
    message = 'New Alarm(s): \n'

    for alarm in _list:
        device = alarm[1]
        severity = alarm[2]
        description = alarm[3]
        timestamp = alarm[4]

        message += f'\tDeviceIp: \'{device}\',\n' \
                   f'\tDescription: {description},\n' \
                   f'\ttime: \'{timestamp}\'.\n' \
                   f'\tSeverity: {severity}\n\n'

    return message


def _create_db():
    db = DBHandler().open_connection()
    db.create_alarm_table()
    db.close_connection()


def _update_alarms_table_notified(_list):
    ids = []
    for alarm in _list:
        ids.append(alarm[0])

    db = DBHandler().open_connection()
    db.update_notified_by_ID(ids)
    db.close_connection()


def __notificationThread(_delay):
    """
    worker definition for thread task

    @param _delay: it specifies the delay in which the task will be performed
    @return: void
    """
    next_time = time.time() + _delay

    notification_manager = NotificationManager()
    config_manager = ConfigManager()

    severity_threshold = config_manager.get_severity_notification_threshold()

    while True:
        time.sleep(max(0, next_time - time.time()))  # making the thread not wasting CPU cycles
        db = DBHandler()

        try:
            db.open_connection()

            result = db.select_alarm_by_severity_unnotified(severity_threshold)

            if len(result) != 0:  # it means that there are some alarms that need to be notified!
                notification_manager.notify(_build_new_alarm_msg(result))
                _update_alarms_table_notified(result)

        except Exception as e:
            traceback.print_exc()
            logging.exception("Problem while trying notify alarms' data." + str(e))

        finally:
            db.close_connection()

        next_time += (time.time() - next_time) // _delay * _delay + _delay  # next scheduling


def main():

    # create if does not exist the local.db
    _create_db()

    # starting thread to fetch netconf data from devices
    threads = alarm_library.start_threads()

    # starting the notifier thread
    notifier = threading.Thread(target=lambda: __notificationThread(5))
    notifier.start()

    threads.append(notifier)

    try:

        # the bot needs to be inside the main thread for signalling purposes
        telegram_bot_service.main()

    except Exception as e:
        logging.log(logging.INFO, 'Could not start the bot!' + str(e))

    finally:
        for t in threads:  # wait for all the threads to join
            t.join()


if __name__ == "__main__":
    main()


