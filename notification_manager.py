"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone
"""

import mail_sender_service
import telegram_bot_service
from config_manager import ConfigManager

config_manager = ConfigManager()


def notify(msg="DEBUG FROM NOTIFICATION MANAGER!"):
    _send_mail(msg)
    _broadcast_alarm(msg)


def _send_mail(msg):
    send_email_flag = config_manager.get_notification_params()['Send_email']

    if send_email_flag:
        mail_sender_service.send_mail(msg)


def _broadcast_alarm(msg):
    send_message_flag = config_manager.get_notification_params()['Send_message']

    if send_message_flag:
        telegram_bot_service.send_to_bot_group(msg)


if __name__ == '__main__':
    notify()
