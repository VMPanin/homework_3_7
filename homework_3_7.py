from urllib.parse import urlencode, urljoin
import requests
import os

TOKEN = os.getenv('token_yametrika')


class YMBase:
    MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/data'

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token),
            'User-Agent': 'netology_ym_api',
            'Content-Type': 'application/x-yametrika+json'
        }


class YandexMetrika(YMBase):
    def __init__(self, token):
        self.token = token

    def get_counters(self):
        url = urljoin(self.MANAGEMENT_URL, 'counters')
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        return [
            Counter(self.token, counter_id['id']) for counter_id in response.json()['counters']
        ]

    def create_counter(self):
        url = urljoin(self.MANAGEMENT_URL, 'counters')
        headers = self.get_headers()
        params = {
            "counter" : {
                'site': 'www.example.ru',
                'name': 'Наименование счетчика',
            }
        }
        response = requests.post(url, params, headers=headers)
        return response.text


class Counter(YMBase):
    def __init__(self, token, counter_id):
        self.token = token
        self.counter_id = counter_id

    def get_info(self):
        url = urljoin(self.MANAGEMENT_URL, 'counter/{}'.format(self.counter_id))
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        return response.json()

    def get_visits(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()['totals'][0]

    def get_views(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()['data'][0]['metrics'][0]

    def get_users(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()['data'][0]['metrics'][0]


ym = YandexMetrika(TOKEN)
counters = ym.get_counters()
for counter in counters:
    print(counter.get_visits())
    print(counter.get_views())
    print(counter.get_users())

