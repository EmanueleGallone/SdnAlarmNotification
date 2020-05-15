# mail_sender_service.setup()
# mail_sender_service.send_mail()

def send_to_bot_group(msg_content='DEBUG ALARM'):  # IMPORTANT!
    '''with this code you can broadcast to all sdn followers the alarm inside the group'''
    import json
    import requests

    with open('../config/personal_credentials.json', 'r') as file:
        data = json.load(file)
        TOKEN = data['token']
        BOT_CHAT_GROUP_ID = data['bot_group_id']

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    data = {'chat_id': {BOT_CHAT_GROUP_ID}, 'text': {msg_content}}
    r = requests.post(url, data)

    return r.status_code, r.reason

if __name__ == '__main__':
    send_to_bot_group('Fabio and Andrès ♥')