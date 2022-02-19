import requests
import json


class Slack:
    s = requests.session()
    secretURL = None

    def __init__(self, url):
        self.secretURL = url

    # Send text alarm
    def send_text_msg(self, slackAlarm):
        url = self.secretURL
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "text": slackAlarm.description
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        print(rep.text)
        if rep.status_code == 200:
            if rep.text == 'ok':
                # Success
                # print('Message Sent.')
                pass
            else:
                raise Exception('Errcode: {} , Errmsg: {}'.format('500', 'Sent Slack message fail'))
        else:
            raise Exception('Request failed with status_code: {}'.format(rep.status_code))


if __name__ == '__main__':
    pass