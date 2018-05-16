# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymysql
from scrapy import signals

import os

from TourSpider.items import CountryItem ,JdItem,CommItem
from TourSpider.dbhelper import DBHelper

class TourspiderPipeline(object):

    def __init__(self):
        #连接数据库
        self.db=DBHelper()
        self.filename1 = None
        self.filename = None
        if os.path.exists("country.json"):
            os.remove("country.json")
        if os.path.exists("jd.json"):
            os.remove("jd.json")

    def process_item(self, item, spider):

        if isinstance(item, CountryItem):
            self.filename = open("country.json", "ab+")
            jsontext = json.dumps(dict(item), ensure_ascii=False)
            self.filename.write(jsontext.encode("utf-8"))

        elif  isinstance(item, JdItem):
            self.filename1 = open("jd.json", "ab+")
            jsontext = json.dumps(dict(item), ensure_ascii=False)
            self.filename1.write(jsontext.encode("utf-8"))

        elif isinstance(item, CommItem):
            self.db.insert(item)

        return item

    def close_spider(self,spider):
        #self.filename.closed()
        self.filename.closed()
        self.filename1.closed()
        pass
