# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient
import re


class Lesson5Pipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.BDLESSON5

    def process_item(self, item, spider):
        if spider.name == 'prac1_sj':
            item['salary'] = self.ex_money(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def ex_money(self, salary):
        salary = salary.replace(u'\xa0', '')
        if salary.startswith('от'):
            min_value = re.findall(r'\d+', salary)[0]
            max_value = 0
        elif salary.startswith('до'):
            min_value = 0
            max_value = re.findall(r'\d+', salary)[0]
        elif salary == 'na':
            min_value = 'na'
            max_value = 'na'
        elif '—' in salary:
            min_value = re.findall(r'^\d+.\d+', salary.split('—')[0])[0]
            max_value = re.findall(r'\d+', salary.split('—')[1])[0]
        else:
            if not re.findall(r'^\d+', salary):
                min_value = 'na'
                max_value = 'na'
            else:
                min_value = re.findall(r'^\d+', salary)[0]
                max_value = re.findall(r'^\d+', salary)[0]

        return min_value, max_value
