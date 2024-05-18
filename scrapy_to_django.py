import os
import django
import json
from dataScrap import settings as django_settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_settings')
django.setup()


from dataScrap.data_scrap_api.models import Article


def transfer_data():
    # Path to the JSON file containing scraped data
    json_file_path = 'items.json'

    # Read and process the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

        # Loop through each item in the JSON data
        for item in data:
            # Check if the article already exists to avoid duplicates
            if not Article.objects.filter(url=item['url']).exists():
                # Create a new Article object and save it to the database
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
