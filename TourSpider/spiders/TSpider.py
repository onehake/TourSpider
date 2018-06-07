# -*- coding: utf-8 -*-
import json
import re
import os
import lxml.html
import scrapy

from scrapy.http import FormRequest, HtmlResponse
from scrapy.selector import Selector

from TourSpider.items import CountryItem, JdItem, CommItem


class TourspiderSpider(scrapy.Spider):
    count = 1  # 全局变量    初始页数

    name = 'Tspider'
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
        #self.test(3)


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
        country_item = CountryItem()
        country_item['country'] = cou
        country_item['url'] = url
        yield country_item
        print("国家抓取完成")
        pass

    #获取国家景点列表  发送post请求
    def get_jd(self, response ):
        print('开始 post 获取国家景点')
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
        '''中国测试
        myFormData = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': '21536', 'iTagId': '0',
                      'iPage': str(current_count)}
        yield scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
                                 headers=unicornHeader,
                                 method='POST',  # GET or POST
                                 formdata=myFormData,  # 表单提交的数据
                                 callback=self.after_post,
                                 meta={'country': '中国', 'country_url': 21536,
                                       'unicornHeader': unicornHeader, 'current_count': current_count},
                                 # rback=self.error_handle,
                                 # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                 dont_filter=True
                                 )
        '''
        #print('开始 post')


        pass

    # 景点翻页
    def after_post(self, response):
        unicornHeader = response.meta['unicornHeader']
        dic = json.loads(response.body)
        country = response.meta['country']
        url = response.meta['country_url']
        current_count = response.meta['current_count']
        if len(Selector(text=dic['data']['page']).xpath('//span[@class="count"]/span')):
            all_count = int(Selector(text=dic['data']['page']).xpath('//span[@class="count"]/span/text()')[0].extract())
        else:
            all_count = 1

        print(all_count)
        print('页码获取成功')

        for jd_counts in range(all_count):
            jd_count = jd_counts+1
            myFormData = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': url, 'iTagId': '0',
                          'iPage': str(jd_count)}
            # print('开始 post')
            yield scrapy.FormRequest(url="http://www.mafengwo.cn/ajax/router.php",
                                     headers=unicornHeader,
                                     method='POST',  # GET or POST
                                     formdata=myFormData,  # 表单提交的数据
                                     callback=self.after_post_getjd,
                                     meta={'country': country, 'country_url': url,
                                           'unicornHeader': unicornHeader, 'current_count': jd_count},
                                     # rback=self.error_handle,
                                     # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                     dont_filter=True
                                     )

    #获取景点
    def after_post_getjd(self,response):
        unicornHeader = response.meta['unicornHeader']
        dic = json.loads(response.body)
        country = response.meta['country']
        url = response.meta['country_url']
        current_count = response.meta['current_count']

        jd_url = Selector(text=dic['data']['list']).xpath('//li/a/@href').extract()
        jd_name = Selector(text=dic['data']['list']).xpath('//li/a/@title').extract()

        for i in range(len(jd_url)):
            jd_item = JdItem()
            jd_item['country'] = country
            #country.xpath('./@href').re('[0-9]{5}')[0]

            jd_item['url'] = re.findall(r"[0-9]{1,7}", jd_url[i])[0]
            jd_item['name'] = jd_name[i]
            print(jd_item['name'])

            #开始获取评论页数
            # jd_url="http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery181031605621927891037_1525169665109&params={"poi_id": "jd_item['url']"}&_= 1525169665228}"
            #
            '''
            # 故宫测试                                                                                                                                    "poi_id": "3474"} & _ = 1525169665228"
            sjd_url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery18106151865610116586_1526372184319&params={"poi_id":"3474"}&_=1526372184582'
            headers = {
                'Accept - Encoding': 'gzip, deflate',
                'Accept - Language': 'en - US, en;q=0.5',
                'Connection': 'keep - alive',
                'DNT': '1',
                'Host': 'pagelet.mafengwo.cn',
                'Referer': 'http://www.mafengwo.cn/poi/' + url + '.html',

                'User - Agent': 'Mozilla / 5.0(WindowsNT10.0; …)Gecko/20100101 Firefox / 59.0',

            }
            # 评论页循环
            yield FormRequest(url=sjd_url, headers=headers, callback=self.get_comment_count,
                              meta={'country': country, 'jd_name': jd_item['name'],'jd_url':jd_item['url'],
                                    'country_url':url,'unicornHeader': unicornHeader},
                              dont_filter=True)
            '''
            sjd_url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery181011702454390918593_1525247201501&params={"poi_id":'+jd_item['url']+'}&_=1525247201612'
            headers = {
                'Accept - Encoding': 'gzip, deflate',
                'Accept - Language': 'en - US, en;q=0.5',
                'Connection': 'keep - alive',
                'DNT': '1',
                'Host': 'pagelet.mafengwo.cn',
                'Referer': 'http://www.mafengwo.cn/poi/' + url + '.html',
                'User - Agent': 'Mozilla / 5.0(WindowsNT10.0; …)Gecko/20100101 Firefox / 59.0',

            }
            # 评论页循环
            yield FormRequest(url=sjd_url, headers=headers, callback=self.get_comment_count,
                              meta={'country': country, 'jd_name': jd_item['name'], 'jd_url': jd_item['url'],
                                    'country_url': url, 'unicornHeader': unicornHeader},
                              dont_filter=True)


            yield jd_item


        pass
    #获取评论数
    def get_comment_count(self, response):
        jd_url=response.meta['jd_url']
        jd_name=response.meta['jd_name']
        country=response.meta['country']
        country_url=response.meta['country_url']
        back = response.body.decode('utf-8')

        # 正则匹配出所需要的html文档
        p = re.compile('\((.*?)}}\)')

        html = json.loads(p.findall(back)[0] + "}}")['data']['html']
        # print(html)
        comm_all_count = 1
        if len(Selector(text=html).xpath('//span[@class="count"]/span[1]/text()')):
            comm_all_count = int(Selector(text=html).xpath('//span[@class="count"]/span[1]/text()')[0].extract())

        print('景点页码')
        
        for comm_countc in range(comm_all_count):
            comm_count = comm_countc + 1
            if comm_count == 1:
                sjd_url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery181011702454390918593_1525247201501&params={"poi_id":'+jd_url+'}&_=1525247201612'
            else:
                sjd_url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery18103080186012365017_1524305195722&params={"poi_id":'+jd_url+',"page":'+str(comm_count)+',"just_comment":1}&=1524305229292'

            headers = {
                'Accept - Encoding': 'gzip, deflate',
                'Accept - Language': 'en - US, en;q=0.5',
                'Connection': 'keep - alive',
                'DNT': '1',
                'Host': 'pagelet.mafengwo.cn',
                'Referer': 'http://www.mafengwo.cn/poi/' + country_url + '.html',
                'User - Agent': 'Mozilla / 5.0(WindowsNT10.0; …)Gecko/20100101 Firefox / 59.0',

            }
            # 评论页循环
            yield FormRequest(url=sjd_url, headers=headers, callback=self.get_comment,
                              meta={'country': country, 'jd_name': jd_name, 'jd_url': jd_url,
                                    'country_url':country_url},
                              dont_filter=True)


    #获取景点评论
    def get_comment(self, response):
        #jd_url = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery181031605621927891037_1525169665109&params={"poi_id": "jd_item['url'],"page":1,"just_comment":1"}&_= 1525169665228}"
        country=response.meta["country"]
        jd=response.meta["jd_name"]
        back = response.body.decode('utf-8')
        # 正则匹配出所需要的html文档
        p = re.compile('\((.*?)}}\)')
        html = json.loads(p.findall(back)[0] + "}}")['data']['html']
        #print(html)

        comm_name = Selector(text=html).xpath('//a[@class="name"]/text()').extract()
        #comm_star =Selector(text=html).xpath('//li[@class="rev-item.comment-item.clearfix"]/span/@class').extract()
        comm = Selector(text=html).xpath('//p[@class="rev-txt"]/text()').extract()
        comm_time = Selector(text=html).xpath('//div[@class="info clearfix"]/span[@class="time"]/text()').extract()
        print(comm_name)

        for i in range(len(comm)):
            commItem = CommItem()
            commItem['country'] = country
            commItem['jd'] = jd
            commItem['name'] = comm_name[i]
            commItem['content'] = comm[i]
            commItem['time'] = comm_time[i]
            yield commItem


        pass
