import hazm
import mongoengine

from newsCrawler.utils import normalize

persian = set(open('newsCrawler/models/persian').read().split('\n'))
stemfunc = hazm.Stemmer()


# noinspection PyPep8Naming
class newsItem(mongoengine.Document):
    """Basic news model"""
    press = mongoengine.StringField()
    title = mongoengine.StringField()
    text = mongoengine.StringField()
    link = mongoengine.StringField()
    date = mongoengine.DateTimeField()
    newsId = mongoengine.StringField()
    category = mongoengine.StringField()
    description = mongoengine.StringField()
    stemmed = mongoengine.ListField()
    tokenized = mongoengine.ListField()
    finished = mongoengine.BooleanField(default=False)
    isIndexed = mongoengine.BooleanField(default=False)
    isModified = mongoengine.BooleanField(default=False)
    similarDocs = mongoengine.ListField(mongoengine.ReferenceField("newsItem"))
    title_tokenized = mongoengine.ListField()
    three_grams = mongoengine.ListField(default=[])

    meta = {
        'indexes': [
            'title',
            'newsId',
            ],
        'strict': False
    }

    def save(self, token=True, *args, **kwargs):
        if (self.text is not None) and token:
            self.text = normalize(self.text)

            l = []
            for i in hazm.sent_tokenize(self.text):
                for k in hazm.word_tokenize(i):
                    if len(k) > 2 and k not in persian:
                        l.append(k)

            self.tokenized = l
            self.stemmed = [stemfunc.stem(i) for i in self.tokenized]

            # near Detection Tokenization based on titles
            l = []
            for i in hazm.sent_tokenize(self.title):
                for k in hazm.word_tokenize(i):
                    if len(k) > 2 and k not in persian:
                        l.append(k)

            self.title_tokenized = l
            del l

            self.create_three_gram()

        return super(newsItem, self).save(*args, **kwargs)

    def create_three_gram(self):
        l = []
        for i in self.title_tokenized:
            for j in range(len(i)):
                if len(i) == 3:
                    l.append(i)
                    break

                if j + 3 > len(i):
                    break

                l.append(i[j : j + 3])

        self.three_grams = l
        del l
