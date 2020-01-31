# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DoubanItem
from scrapy_redis.spiders import RedisCrawlSpider
import redis

class ReviewSpider(RedisCrawlSpider): #父类要改成redis的spider模版，RedisCrawlSpider
    name = 'review'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/subject/33417046/comments']
    rdb = redis.Redis('192.168.0.200', db=0)
    rdb.lpush('review:start_urls','https://movie.douban.com/subject/33417046/comments')
    #lpush review:start_urls https://movie.douban.com/subject/33417046/comments
    # redis中增加起始字段，才会开始爬取，可以写命令来lpush

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # item = {}
        comment = response.xpath('//span[@class="short"]/text()').extract_first()
        print(comment)
        print('**********************************************************')
        item = DoubanItem()
        item['comment'] = comment
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield  item
