import scrapy
import spacy
from bs4 import BeautifulSoup


class RestOfWorldSpider(scrapy.Spider):
    name = 'restofworld'
    start_urls = ['https://restofworld.org/series/the-rise-of-ai/']

    def parse(self, response):
        articles = response.css('article')
        for article in articles:
            title = article.css('h2::text').get()
            body = article.css('div.article-body').get()
            url = article.css('a::attr(href)').get()
            publication_date = article.css('time::attr(datetime)').get()
            author = article.css('span.author::text').get()
            image_urls = article.css('img::attr(src)').getall()

            body_text = BeautifulSoup(body, 'html.parser').get_text()

            nlp = spacy.load("en_core_web_sm")
            doc = nlp(body_text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]

            yield {
                'title': title,
                'body': body_text,
                'url': url,
                'publication_date': publication_date,
                'author': author,
                'image_urls': image_urls,
                'entities': entities
            }
