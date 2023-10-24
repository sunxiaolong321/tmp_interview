import cv2
import ddddocr
import numpy as np


class Ocr:
    def __init__(self):
        self.__det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)

    # 识别图片
    def identify_picture(self, target_img: bytes, background_img: bytes):
        """
        识别缺口验证码
        :param target_img: 目标图片
        :param background_img: 背景图片
        :return:
        """
        res = self.__det.slide_match(target_img, background_img, simple_target=True)
        return res

    def identify_picture_custom(self, target_img: bytes, background_img: bytes):
        """手动识别验证码
        :param target_img: 目标图片
        :param background_img: 背景图片
        :return:
        """
        img_array = np.frombuffer(target_img, np.uint8)
        img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
        y = np.frombuffer(background_img, np.uint8)
        template = cv2.imdecode(y, cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
        value = cv2.minMaxLoc(res)[2][0]

        # 获取的图片和显示的验证码图片大小有差
        distance = int(value * 365 / 544 + 1)
        return distance
