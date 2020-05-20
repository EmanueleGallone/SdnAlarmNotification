
from models.database_manager import DBHandler
from GUI import GUI_Main as GUI

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

    gui = GUI.gui_thread()
    gui.start()

    # TODO decide whether to stop the service if the GUI is exited or not

    gui.join()


if __name__ == "__main__":
    main()


