# -*- coding: utf-8 -*-
import json
import re

import lxml.html
import scrapy

from scrapy.http import FormRequest, HtmlResponse
from scrapy.selector import Selector

from TourSpider.items import CountryItem, JdItem


class TourspiderSpider(scrapy.Spider):
    count = 1  # 全局变量    初始页数

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
    #获取国家标识
    def parse(self, response):
        for country in response.xpath('//dd[@class="clearfix"]/ul/li/a'):
            #country_item = CountryItem()
            #country_item['country'] = country.xpath('./text()')[0].extract()
            cou = country.xpath('./text()')[0].extract()
            url = str(country.xpath('./@href').re('[0-9]{5}')[0])
            #country_item['url'] = url
            current_count = 1

            curl ='http://www.mafengwo.cn/jd/' + url + '/gonglve.html'
            #yield country_item
            yield response.follow(
                curl,
                headers=self.headers,
                meta={'country': cou, 'country_url': url ,'current_count':current_count},
                callback = self.get_jd

            )
            country_item = CountryItem()
            country_item['country'] = cou
            country_item['url'] = url
            yield country_item

        pass

    #获取国家景点列表  发送post请求
    def get_jd(self, response ):
        print('开始 postsafdddhgfgh')
        country = response.meta['country']
        url = response.meta['country_url']
        current_count = response.meta['current_count']
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
        #print('开始 post')

        yield scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
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


        pass

    # 获取国家景点列表  正式获取
    def after_post(self, response):

        dic = json.loads(response.body)
        country = response.meta['country']
        url = response.meta['country_url']
        current_count = response.meta['current_count']
        jd_url = Selector(text=dic['data']['list']).xpath('//li/a/@href').extract()
        jd_name = Selector(text=dic['data']['list']).xpath('//li/a/@title').extract()

        for i in range(len(jd_url)):
            jd_item = JdItem()
            jd_item['country'] = country
            jd_item['url'] = jd_url[i]
            jd_item['name'] = jd_name[i]
            yield jd_item
            print('写入完成！！！')

        # 判断是否存在下一页
        print('开始判断下一行是否存在')
        next = Selector(text=dic['data']['page']).xpath('//div/a[@calss="pi pg-next"]').extract()
        print(next)
        print('((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))')
        if next:
            current_count = int(response.meta['current_count']) + 1
            print('进入到下一页')

            curl = 'http://www.mafengwo.cn/jd/' + url + '/gonglve.html'
            # yield country_item
            yield response.follow(
                curl,
                dont_filter=True,
                meta={'country': country, 'country_url': url, 'current_count': current_count},
                callback=self.get_jd
            )
        else:
            print ('没有下一页')

    #获取景点评论
    def get_comment(self0):

        pass


'''
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




        print('开始国家内 运行')
        for country_item in countryitems:#国家间的循环

            re_url = 'http://www.mafengwo.cn/jd/' + country_item.get('url') + '/gonglve.html'
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
                'X-Requested-With': 'XMLHttpReque',
                'Referer': re_url,
            }

            current_count = 1

            myFormData = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': country_item['url'], 'iTagId': '0',
                          'iPage': str(current_count)}

            yield scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
                                     headers=unicornHeader,
                                     method='POST',  # GET or POST
                                     formdata=myFormData,  # 表单提交的数据
                                     callback=self.after_post,
                                     meta={'country': country_item['country'], 'country_url':country_item['url'],
                                           'unicornHeader':unicornHeader, 'current_count':current_count},
                                     # er
                                     # rback=self.error_handle,
                                     # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                     dont_filter=True
                                     )


     #遍历 items 获取每个 国家的景点


    def after_post(self, response):

        dic = json.loads(response.body)
        country = response.meta['country']
        jd_url =Selector(text=dic['data']['list']).xpath('//li/a/@href').extract()
        jd_name =Selector(text=dic['data']['list']).xpath('//li/a/@title').extract()

        for i in range(len(jd_url)):
            jd_item = JdItem()
            jd_item['country']= country
            jd_item['url']= jd_url[i]
            jd_item['name']= jd_name[i]
            yield jd_item
            print('写入完成！！！')

        #判断是否存在下一页
        print('开始判断下一行是否存在')
        next = Selector(text=dic['data']['page']).xpath('//div/a[@calss="pi pg-next"]').extract()

        log.msg(type(next))
        if  len(next):
            response.meta['current_count'] +=1
            myFormData = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': response.meta['country_url'], 'iTagId': '0',
                          'iPage': response.meta['current_count']}
            print('进入到下一页')

            yield scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
                                     headers=response.meta['unicornHeader'],
                                     method='POST',  # GET or POST
                                     formdata=myFormData,  # 表单提交的数据
                                     callback=self.after_post,
                                     meta={'country': response.meta['country'], 'country_url':response.meta['country_url'],
                                            'unicornHeader':response.meta['unicornHeader'],'current_count':response.meta['current_count']},
                                     # er
                                     # rback=self.error_handle,
                                     # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                     dont_filter=True
                                     )
'''