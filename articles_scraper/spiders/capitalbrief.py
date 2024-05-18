import scrapy
import spacy
from bs4 import BeautifulSoup
from datetime import datetime
from articles_scraper.items import ArticleItem


class CapitalBriefSpider(scrapy.Spider):
    name = 'capitalbrief'
    start_urls = ['https://www.capitalbrief.com/technology/']

    def parse(self, response):
        articles = response.css('div.article')
        for article in articles:
            article_url = article.css('a::attr(href)').get()
            if article_url:
                yield response.follow(article_url, self.parse_article)

    def parse_article(self, response):
        title = response.css('h1.article-title::text').get()
        body = response.css('div.article-body').get()
        url = response.url
        publication_date_str = response.css('time.publication-date::attr(datetime)').get()
        author = response.css('span.author::text').get()
        image_urls = response.css('div.article-body img::attr(src)').getall()

        body_text = BeautifulSoup(body, 'html.parser').get_text()

        if publication_date_str:
            try:
                publication_date = datetime.fromisoformat(publication_date_str)
            except ValueError:
                publication_date = None
        else:
            publication_date = None

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(body_text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        item = ArticleItem(
            title=title,
            body=body_text,
            url=url,
            publication_date=publication_date,
            author=author,
            image_urls=image_urls,
            entities=entities
        )

        yield item
