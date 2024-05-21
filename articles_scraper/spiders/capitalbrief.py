import scrapy
from articles_scraper.items import ArticleItem


class CapitalBriefSpider(scrapy.Spider):
    name = 'capitalbrief'
    start_urls = ['https://www.capitalbrief.com/technology/']

    def parse(self, response, *args, **kwargs):

        articles = response.css("article")
        for article in articles:
            article_url = article.css("h2 a::attr(href)").get()
            yield response.follow(article_url, self.parse_article)

        next_page = response.css('a.btn-more::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        body = response.css('div.content p::text').get()
        url = response.url
        publication_date_str = response.css('time::attr(datetime)').get()
        author = response.css('.author::text').get()
        image_urls = response.css('img::attr(src)').getall()

        title = title.strip()
        body = body.strip()
        author = author.replace('\xa0', ' ').strip()

        if image_urls:
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
