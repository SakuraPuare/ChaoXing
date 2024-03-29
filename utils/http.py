import random

import httpx
from httpx import Response, request, ConnectTimeout, ConnectError

from utils.logger import logger

TIMEOUT = 10


def anti_spider():
    http = Http()
    rq = http.get(f'https://mooc1.chaoxing.com/processVerifyPng.ac?t={random.randint(0, 2147483646)}')
    pass


class Http:
    _instance = None
    HEADER = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 '
                      'Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'cookies'):
            self.cookies = httpx.Cookies()

    def update_cookies(self, cookies: httpx.Cookies = httpx.Cookies()) -> None:
        self.cookies = cookies

    def get(self, url: str, *, params: dict = None, headers: dict = None, cookies: httpx.Cookies = None,
            follow_redirects: bool = True) -> Response:
        h = dict(self.HEADER)
        if headers:
            h.update(headers)

        if not cookies:
            cookies = self.cookies

        try:
            rq = request("GET", url, params=params, headers=h, cookies=cookies, follow_redirects=follow_redirects
                         , timeout=TIMEOUT)

            if 'antispider' in str(rq.url):
                logger.warning('Anti-Spider')
                anti_spider()
                return Response(403)

            return rq
        except (ConnectTimeout, ConnectError) as e:
            logger.error(f'Connect Error, Retry..., {e}')
            # retry
            return self.get(url, params=params, headers=headers, cookies=cookies, follow_redirects=follow_redirects)

    def post(self, url: str, *, data: dict = None, json: dict = None, params: dict = None, headers: dict = None,
             cookies: dict = None, follow_redirects: bool = True) -> Response:
        h = dict(self.HEADER)
        if headers:
            h.update(headers)

        if not cookies:
            cookies = self.cookies

        try:
            rq = request("POST", url, data=data, json=json, params=params, headers=headers, cookies=cookies,
                         follow_redirects=follow_redirects, timeout=TIMEOUT)

            return rq
        except ConnectTimeout | ConnectError as e:
            logger.error(f'Connect Error, Retry..., {e}')
            # retry
            return self.post(url, data=data, json=json, params=params, headers=headers, cookies=cookies,
                             follow_redirects=follow_redirects)
