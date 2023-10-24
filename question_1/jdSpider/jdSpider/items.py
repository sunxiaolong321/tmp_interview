# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 颜色
    color = scrapy.Field()
    # 尺寸
    size = scrapy.Field()
    # 网站货号
    sku = scrapy.Field()
    # 详情
    img_urls = scrapy.Field()
    # 链接
    url = scrapy.Field()
    shop_id = scrapy.Field()
