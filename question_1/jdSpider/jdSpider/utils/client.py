# !bin/bash
# 浏览器登录
import base64
import random
import time
import logging

import numpy as np
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from jdSpider.utils.ocr import Ocr

logger = logging.getLogger(__name__)


class Client:
    """
    实现浏览器自动化
    """

    def __init__(self):
        self.__driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager().install())
        )

    def login(self, username: str, password: str) -> bool:
        """
        实现用户自动登录

        :param username: 用户名
        :param password: 密码
        """
        self.__driver.get(
            "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F"
        )
        self.__driver.find_element(by=By.ID, value="loginname").send_keys(username)
        self.__driver.find_element(by=By.ID, value="nloginpwd").send_keys(password)
        self.__driver.find_element(by=By.ID, value="loginsubmit").click()

        next = input("收到输入验证码")

        if next.lower() == "y":
            return True

        # for i in range(5):
        #     logger.info("正在尝试识别验证码")
        #     self.__pass_verification()
        #     if "https://passport.jd.com/new/login.aspx" not in self.__driver.current_url:
        #         logger.info("验证码识别成功")
        #         break

    def get_cookies(self):
        return self.__driver.get_cookies()

    def __pass_verification(self):
        """
        通过验证码
        """
        time.sleep(2)

        # 拿到图像
        background_img = self.__driver.find_element(
            by=By.CSS_SELECTOR, value=".JDJRV-bigimg > img"
        ).get_attribute("src")
        # 拿到缺口图形
        target_img = self.__driver.find_element(
            by=By.CSS_SELECTOR, value=".JDJRV-smallimg > img"
        ).get_attribute("src")

        background_img_bytes = base64.b64decode(background_img.split(",")[1])
        target_img_bytes = base64.b64decode(target_img.split(",")[1])

        coordinate = Ocr().identify_picture_custom(
            target_img_bytes, background_img_bytes
        )

        btn = self.__driver.find_element(
            by=By.CSS_SELECTOR, value=".JDJRV-slide-inner.JDJRV-slide-btn"
        )

        # 移动坐标
        ActionChains(self.__driver).click_and_hold(btn).move_by_offset(
            coordinate, 0
        ).release().perform()
        time.sleep(1)

        logger.info("需要移动距离：", coordinate)

        act = ActionChains(self.__driver)
        act.click_and_hold(btn).perform()

        _, tracks = RandomTracker().get_tracks(coordinate, 2)

        for e in tracks:
            act.move_by_offset(e, random.randrange(-3, 3)).perform()
        act.pause(1).release().perform()


class RandomTracker:
    def __ease_out_quad(self, x):
        return 1 - (1 - x) * (1 - x)

    def __ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)

    def __ease_out_expo(self, x):
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    def __ease_out_bounce(self, x):
        n1 = 7.5625
        d1 = 2.75
        if x < 1 / d1:
            return n1 * x * x
        elif x < 2 / d1:
            x -= 1.5 / d1
            return n1 * x * x + 0.75
        elif x < 2.5 / d1:
            x -= 2.25 / d1
            return n1 * x * x + 0.9375
        else:
            x -= 2.625 / d1
            return n1 * x * x + 0.984375

    def __ease_in_out_bounce(self, x):
        return (
            (1 - self.__ease_out_bounce(1 - 2 * x)) / 2
            if x < 0.5
            else (1 + self.__ease_out_bounce(2 * x - 1)) / 2
        )

    def get_tracks(self, distance, seconds):
        """
        可以根据滑块的偏移，需要的时间（相对时间，并不是准确时间），以及要采用的缓动函数生成拖动轨迹。

        :param distance: 位移距离
        :param seconds: 时间秒
        :par
        am ease_func: 调用的缓慢函数
        :return:
        """
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            offset = round(self.__ease_in_out_bounce(t / seconds) * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        return offsets, tracks


if __name__ == "__main__":
    print(ChromeDriverManager().install())
