# -*- coding: utf-8 -*-
import re

import scrapy
import json

from cssselect import Selector
from TourSpider.items import CountryItem, JdItem

class MA(scrapy.Spider):
    name = 'mafengwo'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://www.mafengwo.cn/mdd/']
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    Content_Type = 'application/x-www-form-urlencoded'
    Accept_Encoding = 'gzip, deflate'
    headers = {
        'User-Agent': user_agent,
        'Content-Type': Content_Type,
        'Accept-Encoding': Accept_Encoding
    }

    def test(self, count):
        print('测试算定义')
        print(count)
    #获取各个国家标识
    def parse(self, response):
        for country in response.xpath('//dd[@class="clearfix"]/ul/li/a'):
            cou = country.xpath('./text()')[0].extract()
            url = str(country.xpath('./@href').re('[0-9]{5}')[0])
            self.get_jd(cou, url)
            #self.test(3)
            print('ccccccccccccc')


    #获取各个国家景点标识
    def get_jd(self, country, url, current_count=1):
        print('进入 get_jd')
        re_url = 'http://www.mafengwo.cn/jd/' + url + '/gonglve.html'
        unicornHeader = {
            'Accept': 'application/json,text/javascript,*/*;q = 0.01',
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'en-US,en;q=0.5',
            'Cache - Control': 'max - age = 0',
            'Connection': 'keep - alive',
            'Content - Length': '66',
            'Content - Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1',
            'Host': 'www.mafengwo.cn',
            'User - Agent': ' Mozilla / 5.0(WindowsNT10.0; …) Gecko / 20100101Firefox / 59.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': re_url,
        }
        myFormData = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': url, 'iTagId': '0',
                      'iPage': str(current_count)}
        print('开始 post')
        return scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
                                 headers=unicornHeader,
                                 method='POST',  # GET or POST
                                 formdata=myFormData,  # 表单提交的数据
                                 callback=self.after_post,
                                 meta={'country': country, 'country_url': url,
                                       'unicornHeader': unicornHeader, 'current_count': current_count},
                                 # rback=self.error_handle,
                                 # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                 dont_filter=True
                                 )


    #处理返回的post请求
    def after_post(self,response):
        print('处理post结果')



    #获取各个景点评论
    def get_comment(self):
        pass
