"""
Copyright (c) Emanuele Gallone 05-2020.
Author Emanuele Gallone
"""

import smtplib
import json
import logging
from email.message import EmailMessage
from config_manager import ConfigManager

# todo: I know. it all needs a refactor.

logging.basicConfig(filename="log.log", level=logging.ERROR)


def send_mail(msg_body, msg_subject='SDN Alarm notification'):
    config_manager = ConfigManager()

    if msg_body is None:
        raise Exception("you need to specify the the email body!")

    debug_mode = config_manager.get_debug_mode()

    if debug_mode:  # use my personal credentials
        try:
            with open("personal_credentials.json") as json_data_file:
                data = json.load(json_data_file)
                email_address_sender = str(data['email'])
                email_password_sender = str(data['password'])
                email_address_receiver = str(data['email'])  # not a typo, I'm sending notifications to myself
                smtp_server = 'smtp.office365.com'
                smtp_port = 587
        except Exception as e:
            print("something went wrong reading personal_credentials.json file! ->" + str(e))

    else:  # Use the information inside the config file todo: use the config_manager instead!
        try:
            with open("config.json") as json_data_file:
                data = json.load(json_data_file)['Notification_config']
                email_address_sender = str(data['Sender_email'])
                email_password_sender = str(data['Sender_email_password'])
                email_address_receiver = str(data['Receiver_Email'])
                smtp_server = str(data['SMTP_SERVER'])
                smtp_port = int(data['SMTP_PORT'])
        except Exception as e:
            print("something went wrong reading config.json file! ->" + str(e))


    ################### implementation #######################

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email_address_sender, email_password_sender)

        #  email message setup
        msg = EmailMessage()
        msg['Subject'] = msg_subject
        msg['From'] = email_address_sender
        msg['To'] = email_address_receiver
        msg.set_content(msg_body)

        try:
            smtp.send_message(msg)
        except Exception as e:
            logging.log(logging.WARNING, "Failed to send email!" + str(e))

        smtp.close()


#  you can also use the smtp daemon to perform debugging,
#  to do this open a console and type 'python3 -m smtpd -c DebuggingServer -n localhost:1025
#  and then replace smtplib.SMTP(localhost,1025)
#  comment all smtp.ehlo() smtp.starttls() smtp.ehlo and smtp.login() because they're useless in debugging server
# def send_mail_to_debugging_server():
#     with smtplib.SMTP('localhost', 1025) as smtp:
#
#         subject = 'Alarm Notification'
#         body = 'You have a new major alarm'
#
#         msg = f'Subject: {subject}\n\n{body}'
#
#         smtp.sendmail(EMAIL_ADRRESS_SENDER, EMAIL_ADRRESS_SENDER, msg)
#
#         smtp.close()


if __name__ == "__main__":
    try:
        send_mail('debug from test')
    except Exception as ex:
        print("Error: " + str(ex))