from random import choice
import requests

from throttle import Throttle


class Downloader:
    def __init__(self, delay=5, user_agent='fszdict', proxies=None, timeout=10):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = None
        self.timeout = timeout

    def __call__(self, url, params, num_retries=2):
        self.num_retries = num_retries
        self.throttle.wait(url)
        proxies = choice(self.proxies) if self.proxies else None
        headers = {'User-Agent': self.user_agent}
        result = self.download(url, params, headers, proxies)
        return result['html']

    def download(self, url, params, headers, proxies):
        try:
            resp = requests.get(url, params=params, headers=headers,
                                proxies=proxies, timeout=self.timeout)
            html = resp.text
            if resp.status_code >= 400:
                print('Download error:', resp.text)
                html = None
                if self.num_retries and 500 <= resp.status_code < 600:
                    # recursively retry 5xx HTTP errors
                    self.num_retries -= 1
                    return self.download(url, params, headers, proxies)
        except requests.exceptions.RequestException as e:
            print('Download error:', e)
            return {'html': None, 'code': 500}
        return {'html': html, 'code': resp.status_code}
