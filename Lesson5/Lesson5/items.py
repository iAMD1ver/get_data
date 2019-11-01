# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Lesson5Item(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    vacancy_link = scrapy.Field()
    min_value = scrapy.Field()
    max_value = scrapy.Field()
    company_name = scrapy.Field()
    company_link = scrapy.Field()
    experience = scrapy.Field()
    industry = scrapy.Field()