import scrapy
from articles_scraper.items import ArticleItem


class RestOfWorldSpider(scrapy.Spider):
    name = 'restofworld'
    start_urls = ['https://restofworld.org/series/the-rise-of-ai/']

    def parse(self, response, *args, **kwargs):
        articles = response.css("article")
        for article in articles:
            article_url = article.css("a::attr(href)").get()
            yield response.follow(article_url, self.parse_article)

        previous_page = response.css('div.nav-previous::attr(href)').get()
        if previous_page is not None:
            yield response.follow(previous_page, self.parse)

    def parse_article(self, response):
        title = response.css('#headline::text').get()
        body = response.css('h3::text').get()
        url = response.url
        publication_date_str = response.css('time::attr(datetime)').get()
        author = response.css('.author::text').get()
        image_urls = response.css('img::attr(src)').getall()

        title = title.strip()
        body = body.strip()

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
