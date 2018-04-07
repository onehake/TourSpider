# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TourspiderPipeline(object):

    def __init__(self):
        self.filename = open("country.json", "wb")

    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item), ensure_ascii=False)
        self.filename.write(jsontext.encode("utf-8")) + "\n"
        return item

    def close_spider(self,spider):
        self.filename.close()
