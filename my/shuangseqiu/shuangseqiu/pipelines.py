# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class ShuangseqiuPipeline(object):
    def process_item(self, item, spider):
        print(item,'**************************************')
        itemdict = item['ret']
        lines = ''
        for x in itemdict.keys():
            lines = x
            for num in itemdict[x]:
                lines += ','
                lines += num
        print(lines)
        # for x in item['ret'].value():
        #     lines +=','
        #     lines += x
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        with open('f:/temp/666.csv','a',encoding='utf-8') as f:
            csv.writer(f).writerow(lines)
        return item
