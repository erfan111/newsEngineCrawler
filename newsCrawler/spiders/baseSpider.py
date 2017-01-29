import scrapy
from newsCrawler.models.news import newsItem
from datetime import datetime


class baseSpider(scrapy.Spider):
    """Base Crawler"""

    attributes = None
    name = 'Base Spider'

    def __init__(self, attr, *args, **kwargs):
        super(baseSpider, self).__init__(*args, **kwargs)
        self.attributes = attr
        self.name = self.attributes.name
        self.allowed_domains = self.attributes.allowed_domains


    def start_requests(self):
        for url in self.attributes.urls:
            yield scrapy.Request(url=url, callback=self.parse_RSS, dont_filter=True,
                                 meta={'cat': url.split('/')[self.attributes.category_index]})


    def parse_RSS(self, response):
        for i in response.xpath(self.attributes.rss_item_path):
            ID = i.xpath(self.attributes.id_path).extract()[0].split('/')[self.attributes.id_index]
            if newsItem.objects(newsId=ID).count() == 0:
                a = newsItem(newsId=ID)
                a.category = response.meta['cat']
                a.title = i.xpath(self.attributes.title_path).extract()[0]
                try:
                    a.description = i.xpath(self.attributes.description_path).extract()[0]

                except IndexError:
                    pass

                a.link = i.xpath(self.attributes.link_path).extract()[0]
                try:
                    a.date = datetime.strptime(str(i.xpath(self.attributes.date_path).extract()[0]),
                                               self.attributes.date_model)

                except:
                    try:
                        a.date = datetime.strptime(
                            ' '.join(str(i.xpath(self.attributes.date_path).extract()[0]).split()[:-1]),
                            self.attributes.date_model)

                    except:
                        pass

                a.press = self.name
                a.save()
                print("News %s from %s has saved from rss" % (a.newsId, self.name))
                yield scrapy.Request(url=a.link, callback=self.parse_news, dont_filter=True, meta={"id": ID})


    def parse_news(self, response):
        text = ''
        for p in response.xpath(self.attributes.base_html_path):
            for line in p.xpath(self.attributes.text_path):
                try:
                    text += line.xpath('text()').extract()[0] + '\n'

                except:
                    pass

        if len(text):
            a = newsItem.objects(newsId=response.meta['id'], press=self.name).first()
            a.text = text
            a.finished = True
            a.save()
            print("News %s from %s has finished crawling." % (a.newsId, self.name))
            del a
