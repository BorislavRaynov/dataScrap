import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    publication_date = scrapy.Field()
    author = scrapy.Field()
    image_urls = scrapy.Field()
