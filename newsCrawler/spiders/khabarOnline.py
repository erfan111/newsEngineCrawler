import scrapy

from newsCrawler.models.news import newsItem



# noinspection PyAbstractClass
class KhabarOnline(scrapy.Spider):
    """KhabarOnline Crawler"""

    name = "KhabarOnline"
    allowed_domains = ["khabaronline.ir"]
    urls = [
        "http://khabaronline.ir/RSS",
        "http://khabaronline.ir/RSS/Service/society",
        "http://khabaronline.ir/rss/service/politics",
        "http://khabaronline.ir/rss/service/World",
        "http://khabaronline.ir/rss/service/sport",
        "http://khabaronline.ir/rss/service/science",
        "http://khabaronline.ir/RSS/Service/economy",
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
                a.press = self.name
                a.save()
                print("News %s from %s has saved from rss" % (a.newsId, self.name))
                yield scrapy.Request(url=a.link, callback=self.parse_news, dont_filter=True, meta={"id": news_id})

    def parse_news(self, response):
        text = ''
        for p in response.xpath(
                "/html/body/div[@class='container']/div[@id='wrapper']/div[@class='col-lg-6 col-md-6 col-sm-8']/"
                "div[@class='row']/div[@class='newsBodyCont col-sm-12']/div[@class='body']"):
            for line in p.xpath('p'):
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
