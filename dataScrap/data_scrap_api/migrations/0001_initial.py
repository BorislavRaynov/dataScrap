# Generated by Django 5.0.6 on 2024-05-18 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('url', models.URLField(unique=True)),
                ('publication_date', models.DateTimeField()),
                ('author', models.CharField(max_length=255)),
                ('image_urls', models.JSONField()),
                ('entities', models.JSONField()),
            ],
        ),
    ]