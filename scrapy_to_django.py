import os
import django
import json
from dataScrap import settings as django_settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"{django_settings}")
django.setup()


from dataScrap.data_scrap_api.models import Article


def transfer_data():
    json_file_path = 'items.json'

    with open(json_file_path, 'r') as file:
        data = json.load(file)

        for item in data:
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

    print("Data transfer completed successfully.")


if __name__ == "__main__":
    transfer_data()
