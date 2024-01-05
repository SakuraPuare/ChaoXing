import logging
import pathlib
import pickle

import httpx

from models.Course import Course
from utils import http, aes_encryption, get_soup

LOGIN_CYPER = "u2oh6Vu^HWe4_AES"


class User:
    def __init__(self, username: str = "", password: str = "", cookies: httpx.Cookies = httpx.Cookies()) -> None:
        self.name = ""
        self.ids = ""
        self.username = username
        self.password = password
        self.cookies = cookies

        if password or cookies:
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

        post = http.post('https://passport2.chaoxing.com/fanyalogin', headers=headers, data=data)

        if post.status_code != 200:
            logging.error(f'登录失败，状态码：{post.status_code}')
            return False

        resp = post.json()
        if not resp.get('status'):
            logging.error(resp.get('msg2'))
            return False

        self.cookies = post.cookies
        return self._is_login

    @property
    def _is_login(self) -> bool:
        try:
            get = http.get('https://i.chaoxing.com/base/settings', cookies=self.cookies, follow_redirects=True)
            if 'login' in str(get.url):
                return False

            info = http.get('https://passport2.chaoxing.com/mooc/accountManage', cookies=self.cookies,
                            follow_redirects=True)

            soup = get_soup(info.text)
            if soup.find('span', {'class': 'infoDiv'}):
                self.name = soup.find('span', {'id': 'messageName'}).getText()
                self.ids = soup.find('span', {'id': 'uid'}).getText()
                self.username = soup.find('span', {'id': 'messagePhone'}).getText()

        except Exception as e:
            logging.error(e)
            return False

        self._save_cookies()

        return True

    def _save_cookies(self) -> None:
        cookies_path = pathlib.Path('cookies')
        if not cookies_path.exists():
            cookies_path.mkdir()

        with open(cookies_path / f'{self.username}.cookies', 'wb') as f:
            pickle.dump(list(self.cookies.jar), f)
            # f.write(aes_encryption(json.dumps(dict(self.cookies)), LOGIN_CYPER))

    def _load_cookies(self) -> None:
        cookies_path = pathlib.Path('cookies')
        if not cookies_path.exists():
            cookies_path.mkdir()

        if not (cookies_path / f'{self.username}.cookies').exists():
            return

        try:
            with open(cookies_path / f'{self.username}.cookies', 'rb') as f:
                data = pickle.load(f)
                self.cookies = httpx.Cookies()
                for item in data:
                    self.cookies.jar.set_cookie(item)

                # data = json.loads(aes_decryption(f.read(), LOGIN_CYPER))
                # self.cookies = httpx.Cookies()
                # for key, value in data.items():
                #     self.cookies[key] = value
                # self.cookies.update(data)
        except Exception as e:
            logging.error(e)
            return

    def get_course(self) -> list[Course]:
        course = http.get('https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courses/list', cookies=self.cookies)
        soup = get_soup(course.text)
        course_list = []
        for c in soup.find_all('li', {'class': 'course'}):
            name = c.find('h3').getText()
            url = c.find('h3').find('a').get('href')
            info = [i.get_text().strip() for i in c.find_all('p')]
            if len(info) == 3:
                desc, teacher, classes = info
            else:
                desc, teacher, _, classes = info
            classes = classes.split('班级：')[-1]
            course_list.append(Course(name, url, desc, teacher, classes))

        return course_list
