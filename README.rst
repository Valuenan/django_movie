# Интернет кинотеатр


## Установить зависимости:

```bash
poetry install
```

Провести миграцию:

По умолчанию настроено на базу postgreSQL:
Измените натройки в файле

```bash
django_movie/settings.py (раздел DATABASES)
```

```bash
python manage.py makemigrations
python manage.py migrate
```

Создать суперпользователя:

```bash
python manage.py createsuperuser
```

Запустить веб-сервер проекта:

```bash
python manage.py runserver
```

