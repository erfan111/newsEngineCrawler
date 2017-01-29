import scrapy
from scrapy.crawler import CrawlerProcess
from newsCrawler.spiders.baseSpider import baseSpider
from newsCrawler.models.spider import Spider
from newsCrawler import settings


process = CrawlerProcess({
    'USER_AGENT': settings.USER_AGENT,
    'BOT_NAME': settings.BOT_NAME,
    'SPIDER_MODULES': settings.SPIDER_MODULES,
    'NEWSPIDER_MODULE': settings.NEWSPIDER_MODULE,
    'LOG_LEVE': settings.LOG_LEVEL,
    'DEPTH_PRIORITY': settings.DEPTH_PRIORITY,
    'SCHEDULER_DISK_QUEUE': settings.SCHEDULER_DISK_QUEUE,
    'SCHEDULER_MEMORY_QUEUE': settings.SCHEDULER_MEMORY_QUEUE,
    'ROBOTSTXT_OBEY': settings.ROBOTSTXT_OBEY,
    'DOWNLOAD_DELAY': settings.DOWNLOAD_DELAY
})

for spider in Spider.objects():
    try:
        process.crawl(baseSpider, attr=spider)
        process.start()

    except:
        pass

