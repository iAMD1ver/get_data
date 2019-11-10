# -*- coding: utf-8 -*-

# Взять авито Авто. Собирать с использованием ItemLoader следующие данные:
#
# Название
# Все фото
# параметры Авто
# С использованием output_processor и input_processor реализовать очистку и преобразование данных. Значения цен должны быть в виде числового значения.
#
# Дополнительно:
# Перевести всех пауков сбора данных о вакансиях на ItemLoader и привести к единой структуре.

import scrapy
from scrapy.http import HtmlResponse
from Lesson6.avito.items import AvitoItem
from scrapy.loader import ItemLoader


class AvitoAutoSpider(scrapy.Spider):
    name = 'avito_auto'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@class, "pagination-page js-pagination-next")]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        autos = response.xpath('//a[contains(@class, "description-title-link")]/@href').extract()

        for link in autos:
            yield response.follow(link, self.parse_autos)

    def parse_autos(self, response: HtmlResponse):
        # photos = response.xpath('//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        # temp = AvitoItem(photos=photos)
        # yield temp

        loader = ItemLoader(item=AvitoItem(), response=response)
        loader.add_xpath('photos', '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_xpath('name', '//span[@class="title-info-title-text"]/text()')
        loader.add_xpath('params', 'string(//ul[@class="item-params-list"])')
        loader.add_xpath('price', '//div[@class="item-price"]//span[@class="js-item-price"]/@content')
        yield loader.load_item()
