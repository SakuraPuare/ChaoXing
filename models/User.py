import pathlib
import pickle

from httpx import Cookies

from utils import aes_encryption, get_soup
from utils import httpx, logger

LOGIN_CYPER = "u2oh6Vu^HWe4_AES"


class User:
    def __init__(self, username: str = "", password: str = "", cookies: Cookies = Cookies()) -> None:
        self.name = ""
        self.ids = ""
        self.username = username
        self.password = password
        self.cookies = cookies

        if self.password or self.cookies:
            self.login()

    def __repr__(self):
        return f'<User {self.name} {self.ids} {self.username}>'

    def login(self) -> bool:
        if self.cookies and self._is_login:
            return True

        if self.username:
            self._load_cookies()
            if self._is_login:
                return True

        headers = {
            'Origin': 'https://passport2.chaoxing.com',
            'Referer': 'https://passport2.chaoxing.com/login',
        }

        data = {
            'fid': '-1',
            'uname': aes_encryption(self.username, LOGIN_CYPER),
            'password': aes_encryption(self.password, LOGIN_CYPER),
            'refer': 'https://i.chaoxing.com',
            't': 'true',
            'forbidotherlogin': '0',
            'validate': '',
            'doubleFactorLogin': '0',
            'independentId': '0',
            'independentNameId': '0',
        }

        post = httpx.post('https://passport2.chaoxing.com/fanyalogin', headers=headers, data=data)

        if post.status_code != 200:
            logger.error(f'登录失败，状态码：{post.status_code}')
            return False

        resp = post.json()
        if not resp.get('status'):
            logger.error(resp.get('msg2'))
            return False

        self.cookies = post.cookies

        if not self._is_login:
            logger.error('登录失败，未知错误')
            exit()
        return True

    @property
    def _is_login(self) -> bool:
        try:
            get = httpx.get('https://i.chaoxing.com/base/settings')
            if 'login' in str(get.url):
                return False

            info = httpx.get('https://passport2.chaoxing.com/mooc/accountManage')

            soup = get_soup(info.text)
            if soup.find('span', {'class': 'infoDiv'}):
                self.name = soup.find('span', {'id': 'messageName'}).getText()
                self.ids = soup.find('span', {'id': 'uid'}).getText()
                self.username = soup.find('span', {'id': 'messagePhone'}).getText()

        except Exception as e:
            logger.error(e)
            return False

        self._save_cookies()
        return True

    def _save_cookies(self) -> None:
        cookies_path = pathlib.Path('cookies')
        if not cookies_path.exists():
            cookies_path.mkdir()

        httpx.update_cookies(self.cookies)

        with open(cookies_path / f'{self.username}.cookies', 'wb') as f:
            pickle.dump(list(self.cookies.jar), f)

    def _load_cookies(self) -> None:
        cookies_path = pathlib.Path('cookies')
        if not cookies_path.exists():
            cookies_path.mkdir()

        if not (cookies_path / f'{self.username}.cookies').exists():
            return

        try:
            with open(cookies_path / f'{self.username}.cookies', 'rb') as f:
                data = pickle.load(f)
                self.cookies = Cookies()
                for item in data:
                    self.cookies.jar.set_cookie(item)
                httpx.update_cookies(self.cookies)
        except Exception as e:
            logger.error(e)
            return


