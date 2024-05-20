import scrapy
from articles_scraper.items import ArticleItem


class RestOfWorldSpider(scrapy.Spider):
    name = 'restofworld'
    start_urls = ['https://restofworld.org/series/the-rise-of-ai/']

    def parse(self, response, *args, **kwargs):
        articles = response.css('article')
        for article in articles:
            article_url = article.css('a::attr(href)').get()
            print(article_url)
            if article_url:
                yield response.follow(article_url, self.parse_article)

    def parse_article(self, response):
        title = response.css('#headline::text').get()
        print(title)
        body = response.css('h3::text').get()
        url = response.url
        publication_date_str = response.css('time::attr(datetime)').get()
        author = response.css('.author::text').get()
        image_urls = response.css('img::attr(src)').getall()

        title = title.strip() if title else ''
        body = body.strip() if body else 'no body'
        author = author.replace('\xa0', ' ').strip() if author else 'no author'
        image_urls = [url.strip() for url in image_urls]

        item = ArticleItem(
            title=title,
            body=body,
            url=url,
            publication_date=publication_date_str,
            author=author,
            image_urls=image_urls,
        )

        yield item
