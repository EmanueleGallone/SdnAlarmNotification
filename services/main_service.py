import alarm_library

from models.notification_manager import NotificationManager
from models.database_manager import DBHandler

import logging, os

logfile = os.path.join(os.path.dirname(__file__), 'log.log')
logging.basicConfig(filename=logfile, level=logging.WARNING)

try:
    from services import telegram_bot_service

except ImportError as e:
    logging.log(logging.WARNING, 'Could not find the telegram bot' + str(e))


def _create_db():
    db = DBHandler().open_connection()
    db.create_alarm_table()
    db.close_connection()


def main():

    # create if does not exist the local.db
    _create_db()

    # starting thread to fetch netconf data from devices
    threads = alarm_library.start_threads()

    # starting the notifier thread
    notifier = NotificationManager().start()
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


