# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import ast
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class AvitoPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.BDLESSON6

    def process_item(self, item, spider):
        item['price'] = item['price'][0]

        item['params'] = self.repl(item['params'])
        params_list = item['params'].split('\n')
        params_dict = {}
        for param in params_list:
            if param.find(':') != -1:
                param = param.lstrip()
                param = param.rstrip()
                param = param.split(':')
                key = param[0]
                value = param[1]
                params_dict[key] = value
        item['params'] = params_dict

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def repl(self, params):
        return params.replace(u'\xa0', '')

class DataReworkPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [i[1] for i in results if i[0]]
        return item
