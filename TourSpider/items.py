# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TourspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CountryItem(scrapy.Item):
    # 国家名
    country = scrapy.Field()
    # url
    url = scrapy.Field()

class JdItem(scrapy.Item):
    country = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
class CommItem(scrapy.Item):
    country = scrapy.Field()
    jd = scrapy.Field()
    name = scrapy.Field()

    content = scrapy.Field()
    time = scrapy.Field()