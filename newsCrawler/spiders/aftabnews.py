from datetime import datetime

import scrapy

from newsCrawler.models.news import newsItem



# noinspection PyAbstractClass
class Aftabnews(scrapy.Spider):
    """aftabnews Crawler"""

    name = "Aftabnews"
    allowed_domains = ["aftabnews.ir"]
    urls = [
        "http://aftabnews.ir/fa/rss/allnews",
        "http://aftabnews.ir/fa/rss/1",
        "http://aftabnews.ir/fa/rss/2",
        "http://aftabnews.ir/fa/rss/3",
        "http://aftabnews.ir/fa/rss/4",
        "http://aftabnews.ir/fa/rss/5",
        "http://aftabnews.ir/fa/rss/6",
        "http://aftabnews.ir/fa/rss/7",
        "http://aftabnews.ir/fa/rss/8",
        "http://aftabnews.ir/fa/rss/all/mostvisited",
        "http://aftabnews.ir/fa/rss/1/mostvisited",
        "http://aftabnews.ir/fa/rss/2/mostvisited",
        "http://aftabnews.ir/fa/rss/3/mostvisited",
        "http://aftabnews.ir/fa/rss/4/mostvisited",
        "http://aftabnews.ir/fa/rss/5/mostvisited",
        "http://aftabnews.ir/fa/rss/6/mostvisited",
        "http://aftabnews.ir/fa/rss/7/mostvisited",
        "http://aftabnews.ir/fa/rss/8/mostvisited",
    ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_RSS, dont_filter=True, meta={'cat': url.split('/')[-1]})

    def parse_RSS(self, response):
        for i in response.xpath('/rss/channel/item'):
            news_id = i.xpath('link/text()').extract()[0].split('/')[-2]
            if newsItem.objects(newsId=news_id).count() == 0:
                a = newsItem(newsId=news_id)
                a.category = response.meta['cat']
                a.title = i.xpath('title/text()').extract()[0]
                
                try:
                    a.description = i.xpath('description/text()').extract()[0]
                except:
                    pass

                a.link = i.xpath('link/text()').extract()[0]
                a.date = datetime.strptime(' '.join(str(i.xpath('pubDate/text()').extract()[0]).split()[:-1]),
                                           '%d %b %Y %H:%M:%S')
                a.press = self.name
                a.save()
                print("News %s from %s has saved from rss" % (a.newsId, self.name))
                yield scrapy.Request(url=a.link, callback=self.parse_news, dont_filter=True, meta={"id": news_id})

    def parse_news(self, response):
        text = ''
        for p in response.xpath(
                "/html/body/div[@class='row body_b']/div[@class='container page']/div[@class='inner_content row']/"
                "div[@class='col-xs-36 col-sm-36 col-md-31 pull-left']/div[@class='col_r_inner_news col-xs-36 col-sm-26']/"
                "div[@style='direction: rtl;']/div[@class='body']"):
            for line in p.xpath('div'):
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
