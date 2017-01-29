import mongoengine

from newsCrawler.models.news import newsItem
mongoengine.connect('newsEngine', port=27017)


items = newsItem.objects(finished=True)
for i in items:
    if len(i.three_grams):
        first_set = set(i.three_grams)
        for j in items:
            if i.id != j.id:
                if len(j.three_grams):
                    second_set = set(j.three_grams)
                    union_set = second_set | first_set
                    intersect = second_set & first_set

                    hassan_jacard = float(len(intersect)) / float(len(union_set))
                    if hassan_jacard > 0.3:
                        if i not in j.similarDocs:
                            j.similarDocs.append(i)
                            j.save(False)

                        if j not in i.similarDocs:
                            i.similarDocs.append(j)
                            i.save(False)
