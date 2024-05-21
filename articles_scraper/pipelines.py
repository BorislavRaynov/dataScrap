import spacy
from jsonschema import validate, ValidationError
from scrapy.exceptions import DropItem

nlp = spacy.load("en_core_web_sm")

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


class NERPipeline:

    def process_item(self, item, spider):
        doc = nlp(item['body'])
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        item['entities'] = entities
        return item


class ItemCountPipeline:
    def __init__(self):
        self.item_count = 0
        self.min_items = 20

    def process_item(self, item, spider):
        self.item_count += 1
        if self.item_count >= self.min_items:
            spider.crawler.engine.close_spider(spider, 'collected_minimum_items')
        return item
