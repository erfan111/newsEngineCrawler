import mongoengine

from newsCrawler.models.news import newsItem
mongoengine.connect('newsEngine', port=23432)


items = newsItem.objects()#title_tokenized__size=0)
for i in items:
    if(i):
        print(i.id)
        i.similarDocs = [] 
        i.save(False)
        print("Done")
