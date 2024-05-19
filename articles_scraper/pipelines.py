from jsonschema import validate, ValidationError
from scrapy.exceptions import DropItem
import json

article_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Article",
    "properties": {
        "title": {"type": "string"},
        "body": {"type": "string", "minLength": 1},
        "url": {"type": "string", "format": "uri"},
        "publication_date": {"type": "string"},
        "author": {"type": "string", "minLength": 1},
        "image_urls": {
            "type": "array",
            "items": {"type": "string", "format": "uri"}
        },
    },
    "required": ["title", "body", "url", "publication_date", "author"]
}


class ArticlesScraperPipeline:

    def process_item(self, item, spider):
        try:
            validate(instance=item, schema=article_schema)
        except ValidationError:
            raise DropItem(f"Invalid item found: {item}")
        return item


class DuplicatesPipeline:

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item['url']}")
        else:
            self.urls_seen.add(item['url'])
            return item


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open(f'{spider.name}_articles.json', 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item
