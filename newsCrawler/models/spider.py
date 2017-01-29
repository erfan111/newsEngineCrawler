import mongoengine


class Spider(mongoengine.Document):
    """Spider base model"""
    name = mongoengine.StringField()
    allowed_domains = mongoengine.ListField()
    urls = mongoengine.ListField()
    rss_item_path = mongoengine.StringField()
    id_path = mongoengine.StringField()
    title_path = mongoengine.StringField()
    description_path = mongoengine.StringField()
    link_path = mongoengine.StringField()
    date_path = mongoengine.StringField()
    date_model = mongoengine.StringField()
    base_html_path = mongoengine.StringField()
    text_path = mongoengine.StringField()
    category_index = mongoengine.IntField()
    id_index = mongoengine.IntField()
