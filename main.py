import database_handler
import alarm_library
import config_manager
import notification_manager
import telegram_bot_service

import threading

# todo write the main

if __name__ == "__main__":
    config_manager = config_manager.ConfigManager()

    # starting thread to fetch netconf data from devices
    #threads = alarm_library.start_threads()

    # starting the bot
    #threading.Thread(target=telegram_bot_service.main()).start()


    db_handler = database_handler.DBHandler()
    severity_threashold = config_manager.get_severity_notification_threshold()

    result = db_handler.select_alarm_by_severity_unnotified(severity_threashold)
