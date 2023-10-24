import time
import unittest

from jdSpider.utils.client import Client


class TestClient(unittest.TestCase):
    def test(self):
        browser = Client()
        browser.login("123", "123")
        print(browser.get_cookies())
        time.sleep(100)
