# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import HtmlResponse
from scrapy.http import Request
from Lesson7.gmail.items import GmailItem
from scrapy.loader import ItemLoader

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class GmailSpider(scrapy.Spider):
    name = 'Gmail'
    allowed_domains = ['mail.google.com']

    def start_requests(self):
        driver = webdriver.Firefox(executable_path="/home/dmitrii/Documents/Python/Get_data/Lesson7/geckodriver")
        driver.get('https://mail.google.com/mail/u/0/x/')

        user = driver.find_element_by_id('identifierId')
        user.send_keys('testovoetesto256@gmail.com')
        user.send_keys(Keys.RETURN)

        time.sleep(2)

        password = driver.find_element_by_xpath("//input[@name='password']")
        password.send_keys('Testovoetesto123')
        password.send_keys(Keys.RETURN)

        elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'email')))
        yield Request(driver.current_url, cookies=driver.get_cookies(), callback=self.parse)

    def parse(self, response):
        next_page = response.xpath('//a[contains(@id, "tho")]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        else:
            emails = response.xpath('//a[contains(@id, "subj")]/@href').extract()

        for link in emails:
            yield response.follow(link, self.parse_emails)

    def parse_emails(self, response: HtmlResponse):
        loader = ItemLoader(item=GmailItem(), response=response)
        loader.add_xpath('sender', "//div[@class='sender']/span/text()")
        loader.add_xpath('subject', "//b[@id='cos']/text()")
        loader.add_xpath('message', "//div[@id='body']/text()")
        yield loader.load_item()