from datetime import datetime

import scrapy

from newsCrawler.models.news import newsItem



# noinspection PyAbstractClass
class Farsnews(scrapy.Spider):
    """Farsnews Crawler"""

    name = "Farsnews"
    allowed_domains = ["farsnews.com"]
    urls = [
        "http://www.farsnews.com/RSS",
        "http://www.farsnews.com/rss/world",
        "http://www.farsnews.com/rss/politics",
        "http://www.farsnews.com/rss/universities",
        "http://www.farsnews.com/rss/sports",
        "http://www.farsnews.com/rss/economy",
        "http://www.farsnews.com/rss/foreign-policy",
        "http://www.farsnews.com/rss/culture",
        "http://www.farsnews.com/rss/cyberspace",
        "http://www.farsnews.com/rss/resistance",
    ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_RSS, dont_filter=True, meta={'cat': url.split('/')[-1]})

    def parse_RSS(self, response):
        for i in response.xpath('/rss/channel/item'):
            news_id = i.xpath('link/text()').extract()[0].split('/')[-1]
            if newsItem.objects(newsId=news_id).count() == 0:
                a = newsItem(newsId=news_id)
                a.category = response.meta['cat']
                a.title = i.xpath('title/text()').extract()[0]
                
                try:
                    a.description = i.xpath('description/text()').extract()[0]
                except IndexError:
                    pass

                a.link = i.xpath('link/text()').extract()[0]
                a.date = datetime.strptime(str(i.xpath('pubDate/text()').extract()[0]), '%a, %d %b %Y %H:%M:%S')
                a.press = self.name
                a.save()
                print("News %s from %s has saved from rss" % (a.newsId, self.name))
                yield scrapy.Request(url=a.link, callback=self.parse_news, dont_filter=True, meta={"id": news_id})

    def parse_news(self, response):
        text = ''
        for p in response.xpath(
                "/html/body/div[@class='row']/div[@class='container mainframe']/div[@class='cen-lef-col']/"
                "div[@class='centercolumn col-md-7 col-sm-12 col-xs-12']/div[@class='nwstxtmainpane']/"
                "span[@id='nwstxtBodyPane']"):
            for line in p.xpath('p[@class="rtejustify"]'):
                try:
                    text += line.xpath('text()').extract()[0] + '\n'

                except IndexError:
                    pass

        if len(text):
            a = newsItem.objects(newsId=response.meta['id'], press=self.name).first()
            a.text = text
            a.finished = True
            a.save()
            print("News %s from %s has finished crawling." % (a.newsId, self.name))
            del a
