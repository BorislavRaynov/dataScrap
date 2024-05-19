import scrapy
import spacy
from articles_scraper.items import ArticleItem


class RestOfWorldSpider(scrapy.Spider):
    name = 'restofworld'
    start_urls = ['https://restofworld.org/series/the-rise-of-ai/']

    def parse(self, response, *args, **kwargs):
        articles = response.css('article')
        for article in articles:
            article_url = article.css('a::attr(href)').get()
            if article_url:
                yield response.follow(article_url, self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        body = response.css('h3::text').get()
        url = response.url
        publication_date_str = response.css('time::attr(datetime)').get()
        author = response.css('.author::text').get()
        image_urls = response.css('img::attr(src)').getall()

        # nlp = spacy.load("en_core_web_sm")
        # doc = nlp(body_text)
        # entities = [(ent.text, ent.label_) for ent in doc.ents]

        item = ArticleItem(
            title=title,
            body=body_text,
            url=url,
            publication_date=publication_date_str,
            author=author,
            image_urls=image_urls,
            # entities=entities
        )

        yield item
