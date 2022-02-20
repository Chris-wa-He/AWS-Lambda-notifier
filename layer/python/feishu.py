import requests
import json


class Feishu:
    s = requests.session()
    secretURL = None

    def __init__(self, url):
        self.secretURL = url

    # Send text alarm
    def send_text_msg(self, fsAlarm):
        url = self.secretURL
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "msg_type": "text",
            "content": {
                "text": fsAlarm.description
            }
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        print(rep.text)
        if rep.status_code == 200:
            content = json.loads(rep.content)

            if 'StatusCode' in content and content['StatusCode'] == 0:
                # Success
                pass
            else:
                raise Exception('Errcode: {} , Errmsg: {}'.format(content['code'], content['msg']))
        else:
            raise Exception('Request failed with status_code: {}'.format(rep.status_code))


if __name__ == '__main__':
    pass
