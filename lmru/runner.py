from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lmru import settings
from lmru.spiders import slmru
from lmru.spiders.slmru import SlmruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SlmruSpider)

    process.start()