"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone

Simple bot that broadcast SDN alarm detected using NETCONF protocol
built on top of python-telegram-bot's examples ( https://github.com/python-telegram-bot/python-telegram-bot )
"""

import logging
import json
import requests
import os

from models.database_handler import DBHandler
from models.config_manager import ConfigManager

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# retrieving my personal information to start and contact the bot
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../config/personal_credentials.json')

try:

    with open(filename) as json_data_file:
        data = json.load(json_data_file)
        TOKEN = data['token']  # getting bot token
        BOT_CHAT_GROUP_ID = data['bot_group_id']

except Exception as e:
    logger.log(logging.CRITICAL, "Could not retrieve bot information. Bot will not Answer.")


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    link = 'tg://join?invite=HJpFahAwxvTRLEMOmSiYEA'

    update.message.reply_text('Hi! welcome to the Alarm dispatcher bot. '
                              'It will deliver on your phone major alarms detected from your network devices!\n\n'
                              'type /help to list all the commands.\n\n'
                              'Unfortunately we have an issue broadcasting alarms to single users:\n'
                              '-From Official Telegram API FAQ:\n'
                              '-How can I message all of my bot\'s subscribers at once?\n'
                              '-Unfortunately, at this moment we don\'t have methods for sending bulk messages,'
                              ' e.g. notifications. We may add something along these lines in the future. (...)\n\n'
                              f'Enroll to the private group instead {link} where I notify the alarms to all members!')


def send_single_message(chat_id, content='Alarm Notification : {info}'):
    # using this approach we have to save each chat_id for each subscriber (it's doable but I don't like it)
    # use Ngrok to create tunnels and use the webhook instead
    #  it works but it's slow and idk why
    if chat_id is None:
        raise Exception("chat_id is None!")

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    data = {'chat_id': {chat_id}, 'text': content}
    requests.post(url, data).json()

    """

From Official API FAQ:

    -How can I message all of my bot's subscribers at once?
    -Unfortunately, at this moment we don't have methods for sending bulk messages, e.g. notifications. We may add something along these lines in the future. (...)
    
    SOLUTION:
    use send_to_bot_group()
    
"""


def send_to_bot_group(msg_content='DEBUG ALARM'):
    """with this code you can broadcast to all sdn followers the alarm inside the private group"""

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    data = {'chat_id': {BOT_CHAT_GROUP_ID}, 'text': {msg_content}}
    r = requests.post(url, data)

    return r.status_code, r.reason


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('This bot is designed to send alert retrieved from SDNs\' devices.\n'
                              ' By clicking on \'start\' you subscribed to the automated alarm relay system.\n'
                              ' Of course this is a testing bot, but further commands'
                              ' can be developed in future such as \'unsubscribe\' method or \'seeHistory\' '
                              'Commands Available:\n\n'
                              '/status -> It prints the status of the bot\n'
                              '/summary -> prints a summary of the overall alarms\n')


def status(update, context):
    """Echo the user the bot status."""
    sunglasses_emoji = '\U0001F60E'
    update.message.reply_text("I'm Up and Running! " + sunglasses_emoji)


def summary(update, context):
    """gives the user a summary of alarms"""
    db = DBHandler().open_connection()
    manager = ConfigManager()
    msg = ''

    result = db.count_alarms()
    db.close_connection()

    for res in result:
        mapping = manager.get_severity_mapping(int(res[1]))
        count = res[0]
        msg += f'Severity: {mapping}, #: {count}\n'

    update.message.reply_text('Summary:\n' + msg)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("summary", summary))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
