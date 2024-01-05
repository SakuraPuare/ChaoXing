import logging

import httpx
from httpx import Response, request

HEADER = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 '
                  'Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get(
        url: str,
        *,
        params: dict = None,
        headers: dict = None,
        cookies: httpx.Cookies = None,
        follow_redirects: bool = False,
) -> Response:
    h = dict(HEADER)
    if headers:
        h.update(headers)

    try:
        return request(
            "GET",
            url,
            params=params,
            headers=h,
            cookies=cookies,
            follow_redirects=follow_redirects,
        )
    except Exception as e:
        logging.error(e)


def post(
    url: str,
    *,
    data: dict = None,
    json: dict = None,
    params: dict = None,
    headers: dict = None,
    cookies: dict = None,
    follow_redirects: bool = False,
) -> Response:
    h = dict(HEADER)
    if headers:
        h.update(headers)

    try:
        return request(
            "POST",
            url,
            data=data,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            follow_redirects=follow_redirects,
        )
    except Exception as e:
        logging.error(e)

