# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
# данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Lesson7.gmail import settings
from Lesson7.gmail.spiders.Gmail import GmailSpider

if __name__=='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(GmailSpider)
    process.start()