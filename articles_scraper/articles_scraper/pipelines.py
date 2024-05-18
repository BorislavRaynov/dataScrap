import os
import django
from jsonschema import validate, ValidationError
from dataScrap.data_scrap_api.models import Article


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'articles_api.settings')
django.setup()


article_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Article",
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 1},
        "body": {"type": "string", "minLength": 1},
        "url": {"type": "string", "format": "uri"},
        "publication_date": {"type": "string", "format": "date-time"},
        "author": {"type": "string", "minLength": 1},
        "image_urls": {
            "type": "array",
            "items": {"type": "string", "format": "uri"}
        },
        "entities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "label": {"type": "string"}
                },
                "required": ["text", "label"]
            }
        }
    },
    "required": ["title", "body", "url", "publication_date", "author"]
}


class ArticlesScraperPipeline:

    def process_item(self, item, spider):

        try:
            validate(instance=item, schema=article_schema)
            if not Article.objects.filter(url=item['url']).exists():
                article = Article(
                    title=item['title'],
                    body=item['body'],
                    url=item['url'],
                    publication_date=item['publication_date'],
                    author=item['author'],
                    image_urls=item['image_urls'],
                    entities=item['entities']
                )
                article.save()
            return item
        except ValidationError as e:
            spider.logger.error(f"Validation error: {e.message}")
            raise ValidationError(f"Invalid item found: {item}")
