from mongoengine import *

connect('test_mongo')


class Language(Document):
    meta_name = StringField(max_length=2)
    is_default = BooleanField(default=False)
    name = StringField(max_length=30)


class CategoryPage(Document):
    name = StringField(max_length=50)


class Page(Document):
    category = ReferenceField(CategoryPage)
    title = StringField(required=True)
    name = StringField()
    is_home = BooleanField(default=False)
    url = StringField(max_length=100, unique=True)

    def __str__(self):
        return 'title:{}, category:{}, id:{}, url:{}'.format(self.title, self.category, self.id,  self.url)


class PageLanguage(Document):
    page = ReferenceField(Page)
    language = ReferenceField(Language)
    content = StringField()

    def __str__(self):
        return 'id:{}, page:{}, language:{}, content:{}'.format(self.id, self.page, self.language,  self.content)

