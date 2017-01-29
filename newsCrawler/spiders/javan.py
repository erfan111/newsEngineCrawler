from datetime import datetime

import scrapy

from newsCrawler.models.news import newsItem



# noinspection PyAbstractClass
class Javan(scrapy.Spider):
    """Javan Crawler"""

    name = "Javan"
    allowed_domains = ["yjc.ir"]
    urls = [
        "http://www.yjc.ir/fa/rss/allnews",
        "http://www.yjc.ir/fa/rss/1",
        "http://www.yjc.ir/fa/rss/1/129",
        "http://www.yjc.ir/fa/rss/3",
        "http://www.yjc.ir/fa/rss/4",
        "http://www.yjc.ir/fa/rss/5",
        "http://www.yjc.ir/fa/rss/6",
        "http://www.yjc.ir/fa/rss/7",
        "http://www.yjc.ir/fa/rss/8",
        "http://www.yjc.ir/fa/rss/9",
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
                except IndexError:
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
        for p in response.xpath("/html/body/div[@class='container']/div[@class='row padd_main']/div[@class='row']/"
                                "div[@class='col-xs-12 col-ms-12 col-sm-8 padd_left2']/div[@class='news_p_box']/"
                                "div[@class='news_body_con']/div[@class='body']"):
            for line in p.xpath("div[@style='text-align: justify;']"):
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
