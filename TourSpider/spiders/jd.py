# -*- coding: utf-8 -*-
import json
import re

import lxml.html
import scrapy

from scrapy.http import FormRequest, HtmlResponse
from scrapy.selector import Selector

from TourSpider.items import CountryItem, JdItem, CommItem


class jdSpider(scrapy.Spider):
    name = 'jdspider'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery181011702454390918593_1525247201501&params={"poi_id":"3474"}&_=1525247201612']

    headers = {
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'en - US, en;q=0.5',
        'Connection': 'keep - alive',
        'DNT': '1',
        'Host': 'pagelet.mafengwo.cn',
        'Referer': 'http://www.mafengwo.cn/poi/21536.html',
        'User - Agent': 'Mozilla / 5.0(WindowsNT10.0; …)Gecko/20100101 Firefox / 59.0',

    }
    def parse(self, response):
        print(response.body)
        #print(response.body.status_code)

        back = response.body.decode('utf-8')
        # 正则匹配出所需要的html文档
        p = re.compile('\((.*?)}}\)')
        html = json.loads(p.findall(back)[0] + "}}")['data']['html']
        print(html)
        #dic = json.loads(response.body,encoding="unicode")
        comm_name = Selector(html).xpath(
            '//ul/li[@class="rev-item.comment-item.clearfix"]/a[@class="name"]/text()').extract()
        comm_star = Selector(text=dic['data']['html']).xpath(
            '//ul/li[@class="rev-item.comment-item.clearfix"]/span/@class').extract()
        comm = Selector(text=dic['data']['html']).xpath(
            '//ul/li[@class="rev-item.comment-item.clearfix"]/p[@class="rev-txt"]/text()').extract()
        comm_time = Selector(text=dic['data']['html']).xpath(
            '//ul/li[@class="rev-item.comment-item.clearfix"]/div[@class="info clearfix"]/text()').extract()

        for i in range(len(comm)):
            commItem = CommItem()
            commItem['name'] = comm_name[i]
            commItem['star'] = comm_star[i]
            commItem['content'] = comm[i]
            commItem['time'] = comm_time[i]
            yield commItem


