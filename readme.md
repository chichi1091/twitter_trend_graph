https://api.twitter.com/1.1/search/tweets.json?lang=ja&result_type=mixed&count=100&include_entities=true&until=2018-03-15

## 環境
```sh
python -m venv env
source env/bin/activate
pip install django django-crontab
pip install psycopg2 psycopg2-binary
pip install dj-database-url
pip install gunicorn
pip install python-twitter

pip freeze > requirements.txt
```

## プロジェクト作成
```sh
django-admin startproject twitter_trend_graph
python manage.py startapp dashboards
```

## マイグレーション
```sh
python manage.py makemigrations dashboards
python manage.py sqlmigrate dashboards 0001
python manage.py migrate
```
