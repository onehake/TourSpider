# -*- coding: utf-8 -*-
import scrapy
import re
import json
import lxml.html
from TourSpider.items import CountryItem ,JdItem
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

count = 1  # 全局变量    初始页数


class TourspiderSpider(scrapy.Spider):

    name = 'tourspider'
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
          # 指定处理Response的函数




        print('开始运行')
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

            current_count = 1
            global count
            count = 1
            while True:
                myFormData = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': country_item['url'], 'iTagId': '0',
                              'iPage': str(current_count)}

                yield scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
                                          headers=unicornHeader,
                                          method='POST',  # GET or POST
                                          formdata=myFormData,  # 表单提交的数据
                                          callback=self.after_post,
                                         meta={'country': country_item['country']},
                                          # errback=self.error_handle,
                                          # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                          dont_filter=True
                                          )

                print(count)

                if(current_count >= count):
                    break
                current_count += 1

     #遍历 items 获取每个 国家的景点

    def after_post(self, response):

        dic = json.loads(response.body)
        country = response.meta['country']
        jd_url =Selector(text=dic['data']['list']).xpath('//li/a/@href').extract()
        jd_name =Selector(text=dic['data']['list']).xpath('//li/a/@title').extract()

        for i in range(len(jd_url)):
            jd_item = JdItem()
            jd_item['country']= country
            jd_item['url']= jd_url
            jd_item['name']= jd_name
            yield jd_item
        #判断是否存在下一页
        global count
        if dic['data']['page'] !='':
            #共几页
            count=int(Selector(text=dic['data']['page']).xpath('//div[@class="m-pagination"]/span[1]/span[1]/text()')[0].extract())
        else:
            count=1
        print (count)
        return count
