# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from Lesson5.Lesson5.items import Lesson5ItemSj


class Prac1SjSpider(scrapy.Spider):
    name = 'prac1_sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@class, "f-test-link-dalshe")]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.xpath('//a[contains(@class, "icMQ_ _1QIBo")]/@href').extract()

        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response):
        name = response.xpath('string(//h1[@class="_3mfro rFbjy s1nFK _2JVkc"])').extract_first()

        salary = response.xpath('string(//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"])').extract_first()

        company_name = response.xpath('//h2[@class="_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI"]/text()').extract_first()
        company_link = 'https://superjob.ru' + response.xpath('//h2[@class="_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI"]/parent::*/@href').extract_first()
        experience = response.xpath('//span[@class="_3mfro _1hP6a _2JVkc _3Ll36"]/text()').extract_first()
        industry = None
        vacancy_link = response.url

        yield Lesson5ItemSj(name=name, salary=salary, company_name=company_name,
                          company_link=company_link, experience=experience, industry=industry,
                          vacancy_link=vacancy_link)
