import os
import django
import json
from scrapy.crawler import CrawlerProcess
from articles_scraper.articles_scraper.spiders.restofworld import RestOfWorldSpider
from articles_scraper.articles_scraper.spiders.capitalbrief import CapitalBriefSpider
from dataScrap.data_scrap_api.models import Article

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'articles_api.settings')
django.setup()


process = CrawlerProcess(settings={
    'FEEDS': {
        'items.json': {'format': 'json'},
    },
})

process.crawl(RestOfWorldSpider)
process.crawl(CapitalBriefSpider)
process.start()


with open('items.json') as f:
    articles = json.load(f)
    for article_data in articles:
        article = Article(**article_data)
        article.save()
