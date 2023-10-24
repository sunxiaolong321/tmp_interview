import re
import time

import scrapy
from scrapy import FormRequest, Request

from jdSpider.items import JdSpiderItem
from jdSpider.utils.client import Client
from jdSpider.utils.decrypt.decrypt import decrypt_h5st, aes256


class JdIndexSpider(scrapy.Spider):
    name = "jdIndex"
    allowed_domains = ["jd.com"]

    def __init__(self):
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }
        client = Client()
        client.login("18888888888", "123456")
        self.cookies = client.get_cookies()

    def start_requests(self):
        url = "https://list.jd.com/list.html?cat=1318,12099,9756"
        yield Request(
            url,
            headers=self.headers,
            cookies=self.cookies,
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response):
        goods_list = (
            response.css(".gl-item > .gl-i-wrap > div.p-img > a")
            .xpath("@href")
            .getall()
        )
        self.logger.info(f"当前页面商品数量：{len(goods_list)}")

        for goods_url in goods_list:
            if goods_url.startswith("//"):
                goods_url = "https:" + goods_url
                yield Request(
                    goods_url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse_detail,
                    dont_filter=True,
                )

    def parse_detail(self, response):
        item = JdSpiderItem()
        item["url"] = response.url
        item["title"] = response.xpath('//div[@class="sku-name"]/text()').get().strip()
        # item['price'] = response.css(".p-price > .price:nth-child(1)::text").get()
        item["color"] = (
            response.css("#choose-attr-1 > .dd > .item").xpath("@data-value").getall()
        )
        item["size"] = (
            response.css("#choose-attr-2 > .dd > .item").xpath("@data-value").getall()
        )
        item["img_urls"] = response.css(".lh > li > img").xpath("@src").getall()
        item["sku"] = re.search("\d+", response.url)[0]
        item["shop_id"] = response.css(".follow-shop").xpath("@data-vid").get()

        mba_muid = list(filter(lambda x: x.get("name") == "__jdu", self.cookies))[
            0
        ].get("value")

        sku = re.search("\d+", response.url)[0]
        security_token = list(
            filter(lambda x: x.get("name") == "shshshfpb", self.cookies)
        )[0].get("value")

        t = int(time.time() * 10**3)

        vender_id = re.search("venderId:(\d+),", response.text)[1]

        body = {
            "skuId": sku,
            "cat": "1318,12099,9756",
            "area": "13_1032_1039_57817",
            "shopId": item["shop_id"],
            "venderId": int(vender_id),
            "paramJson": '{\\"platform2\\":\\"1\\",\\"specialAttrStr\\":\\"p0p1pppppp1ppp1pppppppppppppp\\",'
                         '\\"skuMarkStr\\":\\"00\\"}',
            "num": 1,
            "bbTraffic": "",
        }

        formdata = {
            "appid": "pc-item-soa",
            "functionId": "pc_detailpage_wareBusiness",
            "client": "pc",
            "clientVersion": "1.0.0",
            "t": str(t),
            "body": str(body).replace("'", '"').replace(" ", ""),
            "h5st": decrypt_h5st(
                {
                    "appid": "pc-item-soa",
                    "body": aes256(str(body).replace("'", '"')).replace(" ", ""),
                    "client": "pc",
                    "clientVersion": "1.0.0",
                    "functionId": "pc_detailpage_wareBusiness",
                    "t": t,
                }
            ),
            "x-api-eid-token": security_token,
            "loginType": "3",
            "uuid": list(filter(lambda x: x.get("name") == "__jda", self.cookies))[
                0
            ].get("value"),
        }

        self.logger.info(f"formdata：{formdata}")

        yield FormRequest(
            url="https://api.m.jd.com",
            method="GET",
            formdata=formdata,
            headers=self.headers,
            cookies=self.cookies,
            callback=self.parse_price,
            dont_filter=True,
            meta={"item": item},
        )

    def parse_price(self, response):
        item = response.meta["item"]
        # item['price']

        return item
