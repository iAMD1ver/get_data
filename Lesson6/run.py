from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Lesson6.avito import settings
from Lesson6.avito.spiders.avito_auto import AvitoAutoSpider

if __name__=='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoAutoSpider)
    process.start()
