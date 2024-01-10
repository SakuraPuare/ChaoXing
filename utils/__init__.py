import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from bs4 import BeautifulSoup

from utils.http import Http
from utils.logger import logger

httpx = Http()


def aes_encryption(message: str, key: str) -> str:
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv=key.encode('utf-8'))
    encrypted = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')


def aes_decryption(message: str, key: str) -> str:
    message = base64.b64decode(message)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv=key.encode('utf-8'))
    decrypted = unpad(cipher.decrypt(message), AES.block_size)
    return decrypted.decode('utf-8')


def get_soup(text: str) -> BeautifulSoup:
    return BeautifulSoup(text, 'html.parser')
