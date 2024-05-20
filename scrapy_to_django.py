import subprocess
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataScrap.settings')
django.setup()


from dataScrap.data_scrap_api.models import Article


def transfer_data(spider_name: str):
    json_file_path = f"{spider_name}_articles.json"

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for item in data:
            if not Article.objects.filter(url=item['url']).exists():
                Article.objects.create(
                    title=item['title'],
                    body=item['body'],
                    url=item['url'],
                    publication_date=item['publication_date'],
                    author=item['author'],
                    image_urls=item['image_urls'],
                    entities=item.get('entities', [])
                )

    print("Data transfer completed successfully.")


if __name__ == "__main__":
    subprocess.run(["scrapy", "crawl", "capitalbrief", "-o", "capitalbrief_articles.json"])
    subprocess.run(["scrapy", "crawl", "restofworld", "-o", "restofworld_articles.json"])
    transfer_data("capitalbrief")
    transfer_data("restofworld")
