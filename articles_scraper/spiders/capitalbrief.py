import scrapy
from articles_scraper.items import ArticleItem


class CapitalBriefSpider(scrapy.Spider):
    name = 'capitalbrief'
    start_urls = ['https://www.capitalbrief.com/technology/']
    articles_count = 0
    min_articles = 20

    def parse(self, response, *args, **kwargs):
        articles = response.css('article')
        for article in articles:
            if self.articles_count < self.min_articles:
                article_url = article.css('a::attr(href)').get()
                if article_url:
                    yield response.follow(article_url, self.parse_article)
            else:
                break

        # if self.articles_count < self.min_articles:
        #     next_page = response.css('a.next::attr(href)').get()
        #     if next_page:
        #         yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        body = response.css('section p::text').get()
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
