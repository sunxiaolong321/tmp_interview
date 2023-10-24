import unittest

from jdSpider.utils.decrypt.decrypt import decrypt_h5st


class TestClient(unittest.TestCase):
    def test_decrypt_h5st(self):
        decrypt_h5st("")
