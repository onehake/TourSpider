# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from TourSpider.items import CountryItem ,JdItem

class TourspiderPipeline(object):

    def __init__(self):
        self.filename= None
    def process_item(self, item, spider):
        if isinstance(item, CountryItem):
            self.filename = open("country.json", "ab+")
            jsontext = json.dumps(dict(item), ensure_ascii=False)
            self.filename.write(jsontext.encode("utf-8"))

        elif  isinstance(item, JdItem):
            self.filename = open("jd.json", "ab+")
            jsontext = json.dumps(dict(item), ensure_ascii=False)
            self.filename.write(jsontext.encode("utf-8"))

        return item

    def close_spider(self,spider):
        #self.filename.closed()
        pass

