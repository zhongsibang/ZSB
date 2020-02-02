# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ShuangseqiuItem

class ReviewSpider(CrawlSpider):
    name = 'review'
    allowed_domains = ['zhcw.com']
    start_urls = ['http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'pageNum=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        dates = response.xpath('//td[2]/text()')
        nums = response.xpath('//td/em/text()')
        print(dates,nums)
        rets = []
        retssss = []
        for num in nums:
            if len(rets)>6:
                retssss.append(rets)
                rets=[]
            ret = num.extract()
            rets.append(ret)
        retssss.append(rets)
        for i in range(len(dates)):
            item = ShuangseqiuItem()
            item['ret'] = {dates[i].extract():retssss[i]}
            yield item
