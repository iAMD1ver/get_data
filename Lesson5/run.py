from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Lesson5.Lesson5 import settings
from Lesson5.Lesson5.spiders.prac1_hh import Prac1HhSpider

if __name__=='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(Prac1HhSpider)
    process.start()
