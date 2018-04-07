# -*- coding: utf-8 -*-
import scrapy
import re
from TourSpider.items import CountryItem
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
import json

class TourspiderSpider(scrapy.Spider):
    name = 'tourspider'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://www.mafengwo.cn/mdd/']
    url = 'http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    #cookie = 'ASP.NET_SessionSvc=MTAuOC4xODkuNTZ8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTUwMDU0MDAxMTY4Mg; ASP.NET_SessionId=llp1osc0ejrpnx514beculek; _abtest_userid=6ba3a6e7-b467-43c7-a7a5-f9df2b6539f4; _bfi=p1%3D100003%26p2%3D0%26v1%3D1%26v2%3D0; bdshare_firstime=1511921790715; _ga=GA1.2.1170534963.1511921792; _gid=GA1.2.1773672486.1511921792; MKT_Pagesource=PC; appFloatCnt=1; manualclose=1; _bfa=1.1511852470959.vij5.1.1511921789102.1511966978022.3.3; _bfs=1.1; page_time=1511852472334%2C1511921790642%2C1511966980133; _RF1=119.36.214.6; _RSG=HYKTjJ9ngFFxfmOUr9OoA9; _RDG=289caa714119b022b402ce802a4784c45c; _RGUID=f3eac494-ed75-4891-92b2-609d5e630a7b; Session=smartlinkcode=U135371&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4899&SID=135371&OUID=&Expires=1512571780659; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224899%22%2C%22timestamp%22%3A1511966980680%7D%5D; _jzqco=%7C%7C%7C%7C%7C1.1134122519.1511921791839.1511921791840.1511966980795.1511921791840.1511966980795.0.0.0.2.2; __zpspc=9.2.1511966980.1511966980.1%233%7Cwww.google.com%7C%7C%7C%7C%23'
    Content_Type = 'application/x-www-form-urlencoded'
    Accept_Encoding = 'gzip, deflate'
    headers = {
        'User-Agent': user_agent,
        #'Cookie': cookie,
        'Content-Type': Content_Type,
        'Accept-Encoding': Accept_Encoding
    }



    def parse(self, response):
        '''
        #site = response.xpath('/')
        for url in response.xpath('//dd[@class="clearfix"]/ul/li/a/text()').extract():
            print(url)
        for country in response.xpath('//dd[@class="clearfix"]/ul/li/a/@href'):
            print(country.re('[0-9]{5}'))
        '''
        #遍历获取 国家名 url
        countryitems = []
        for country in response.xpath('//dd[@class="clearfix"]/ul/li/a'):
            countryitem = CountryItem()
            #print(country.xpath('./text()').extract())
            #print(str(country.xpath('./@href').re('[0-9]{5}')))
            countryitem['country'] = country.xpath('./text()').extract()
            url = str(country.xpath('./@href').re('[0-9]{5}'))
            countryitem['url'] = url
            #url = 'http://www.mafengwo.cn/jd/' + url +'/gonglve.html'
            countryitems.append(countryitem)
            yield countryitem
        #yield countryitems

        url = 'http://www.mafengwo.cn/ajax/router.php'
        #遍历 items 获取每个 国家的景点
        for country_item in countryitems:
            form_data = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': country_item['url'], 'iTagId': '0', 'iPage': '1'}
            scrapy.FormRequest()
            yield scrapy.FormRequest(url, formdata=form_data, headers=self.headers, callback=self.after_post)  # 还可以通过callback修改回调函数等

    def after_post(self, response):
        datas = json.loads(response.text)["data"]["list"]
        for data in datas:
             print(data[""])







    '''
        sel = Selector(response)
        sites = sel.xpath('/dd[@class="clearfix"]/ul/li')
        countryitems = []
        for country in sites:
            countryitem = CountryItem()
            countryitem['country'] = country.xpath('a/text()').extract()
            countryitem['url'] = country.xpath('a/@href').extract()
            countryitems.append(countryitem)
        yield countryitems
       
        url = 'http://www.mafengwo.cn/ajax/router.php'
        form_data = {'sAct': 'KMdd_StructWebAjax%7CGetPoisByTag', 'iMddid': '21536', 'iTagId': '0', 'iPage': '1'}
        yield scrapy.FormRequest(url, formdata=form_data, headers=self.headers, callback=self.after_post)  # 还可以通过callback修改回调函数等


    def after_post(self,response):
        datas = json.loads(response.text)["data"]["list"]
        for data in datas:countryitems = []
            print(data[""])

         count = response.xpath('span[@class="count"]/span[1]/text()')
         print (count)
         page = response.xpath('span[@class="count"]/span[2]/text()')
         print(page)
     


    '''