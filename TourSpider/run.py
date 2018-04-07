# -*- coding: utf-8 -*-

from scrapy import cmdline
name = 'tourspider'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())