tg_request_url = 'https://api.telegram.org/bot{}/sendMessage'


def replace_request_url(bot_id):
    new_url = tg_request_url.format(bot_id)
    print(new_url)


replace_request_url('numberId:uuid')
