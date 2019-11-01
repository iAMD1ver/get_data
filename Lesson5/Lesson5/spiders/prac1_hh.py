# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from Lesson5.Lesson5.items import Lesson5Item


class Prac1HhSpider(scrapy.Spider):
    name = 'prac1_hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=Data+Science']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@class, "HH-Pager-Controls-Next")]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.xpath('//span[contains(@class, "g-user-content")]/a/@href').extract()

        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response):
        name = response.xpath('string(//div[@class="vacancy-title "]/h1[@class="header"])').extract_first()

        if response.xpath('//span[contains(@itemprop, "value")]/meta[contains(@itemprop, "value")]/@content'):
            min_value = 'na'
            max_value = response.xpath(
                '//span[contains(@itemprop, "value")]/meta[contains(@itemprop, "value")]/@content').extract_first()
        elif response.xpath('//meta[contains(@itemprop, "maxValue")]/@content') and response.xpath(
                '//meta[contains(@itemprop, "minValue")]/@content'):
            min_value = response.xpath('//meta[contains(@itemprop, "minValue")]/@content').extract_first()
            max_value = response.xpath('//meta[contains(@itemprop, "maxValue")]/@content').extract_first()
        elif response.xpath('//meta[contains(@itemprop, "minValue")]/@content') and not response.xpath(
                '//meta[contains(@itemprop, "maxValue")]/@content'):
            min_value = response.xpath('//meta[contains(@itemprop, "minValue")]/@content').extract_first()
            max_value = 'na'
        else:
            min_value = 'na'
            max_value = 'na'

        company_name = response.xpath('//span[@itemprop="name"]/text()').extract_first()
        company_link = 'https://hh.ru' + response.xpath('//a[@class="vacancy-company-name"]/@href').extract_first()
        experience = response.xpath('//span[@data-qa="vacancy-experience"]/text()').extract_first()
        industry = response.xpath('//meta[contains(@itemprop, "industry")]/@content').extract()
        vacancy_link = response.url

        yield Lesson5Item(name=name, min_value=min_value, max_value=max_value, company_name=company_name,
                          company_link=company_link, experience=experience, industry=industry, vacancy_link=vacancy_link)
