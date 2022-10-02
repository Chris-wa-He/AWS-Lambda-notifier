import requests
import json


class Telegram:
    s = requests.session()
    secretURL = None

    def __init__(self, url):
        self.secretURL = url

    # Send text alarm
    def send_text_msg(self, chat_id, tg_alarm):
        url = self.secretURL
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "chat_id": chat_id,
            "text": tg_alarm.description
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        print(rep.text)
        if rep.status_code == 200:
            content = json.loads(rep.content)

            if 'ok' in content and content['ok'] is True:
                # Success
                pass
            else:
                raise Exception('Errcode: {} , Errmsg: {}'.format(content['error_code'], content['description']))
        else:
            raise Exception('Request failed with status_code: {}'.format(rep.status_code))


if __name__ == '__main__':
    pass
