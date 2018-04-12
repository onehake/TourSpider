# -*- coding: utf-8 -*-
import scrapy
import re
import json
import lxml.html
from TourSpider.items import CountryItem
from scrapy.http import FormRequest


class TourspiderSpider(scrapy.Spider):
    name = 'tourspider'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://www.mafengwo.cn/mdd/']
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
        #遍历获取 国家名 url
        countryitems = []
        for country in response.xpath('//dd[@class="clearfix"]/ul/li/a'):
            countryitem = CountryItem()
            #print(country.xpath('./text()')[0].extract())
            #Sprint(country.xpath('./@href').re('[0-9]{5}')[0])
            countryitem['country'] = country.xpath('./text()')[0].extract()
            url = str(country.xpath('./@href').re('[0-9]{5}')[0])
            countryitem['url'] = url
            #url = 'http://www.mafengwo.cn/jd/' + url +'/gonglve.html'
            countryitems.append(countryitem)
            yield countryitem
        #yield countryitems


        '''
         # header信息
        unicornHeader = {
            'Host': 'www.mafengwo.cn',
            'Referer': 'http://www.mafengwo.cn/jd/21536/gonglve.html',
        }
        # 表单需要提交的数据
        myFormData = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': '21536', 'iTagId': '0', 'iPage': '1'}

        # 自定义信息，向下层响应(response)传递下去
        #customerData = {'key1': 'value1', 'key2': 'value2'}

        yield scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
                                 headers=unicornHeader,
                                 method='POST',  # GET or POST
                                 formdata=myFormData,  # 表单提交的数据
                                 callback=self.after_post,
                                 #errback=self.error_handle,
                                 # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                 dont_filter=True
                                 )
        url = 'http://www.mafengwo.cn/ajax/router.php'
        '''
        #遍历 items 获取每个 国家的景点


        for country_item in countryitems:#国家间的循环
            re_url= 'http://www.mafengwo.cn/jd/'+country_item.get('url')+'/gonglve.html'
            unicornHeader = {
                'Accept':'application/json,text/javascript,*/*;q = 0.01',
                'Accept - Encoding': 'gzip, deflate',
                'Accept - Language':'en-US,en;q=0.5',
                'Cache - Control': 'max - age = 0',
                'Connection': 'keep - alive',
                'Content - Length': '66',
                'Content - Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'DNT': '1',
                'Host': 'www.mafengwo.cn',
                'User - Agent':' Mozilla / 5.0(WindowsNT10.0; …) Gecko / 20100101Firefox / 59.0',
                'X-Requested-With': 'XMLHttpReque',
                'Referer': re_url,
            }

            myFormData = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': country_item['url'], 'iTagId': '0',
                          'iPage': '1'}
            yield scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
                                      headers=unicornHeader,
                                      method='POST',  # GET or POST
                                      formdata=myFormData,  # 表单提交的数据
                                      callback=self.after_post,
                                      # errback=self.error_handle,
                                      # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                      dont_filter=True
                                      )



    def after_post(self, response):
        print('cccccccccccc')
        dic = json.loads(response.text)
        content = dic["data"]["list"]
        html = lxml.html.fromstring(content)#将json信息渲染成html
        for jd_item in html.cssselect("li.item"):
            print(jd_item.cssselect("a.title")[0].text)
