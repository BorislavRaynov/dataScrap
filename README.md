Python application that extract, transform, load (ETL) and deliver data.

---
HOW TO SET UP AND RUN THE APP
---
1: Running the app on Ubuntu:

    - clone the repo
    - set up virtual environment
    RUN IN CMD THE FOLLOWING COMMANDS:
    - python -m pip install --upgrade pip
    - pip install -r requirements.txt
    - python manage.py makemigrations
    - python manage.py migrate
    - python scrapy_to_django.py
    - python manage.py runserver
---
2: Endpoints:

    - localhost:8000/api/articles/
    - partial functionality on localhost:8000
