import subprocess
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataScrap.settings')
django.setup()


from dataScrap.data_scrap_api.models import Article


def transfer_data():
    json_file_path = 'articles.json'

    with open(json_file_path, 'r') as file:
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
                )

    print("Data transfer completed successfully.")


if __name__ == "__main__":
    subprocess.run(["scrapy", "crawl", "capitalbrief", "-o", "articles.json"])
    # subprocess.run(["scrapy", "crawl", "restofworld", "-o", "articles.json"])
    transfer_data()
