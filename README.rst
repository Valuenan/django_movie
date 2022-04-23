# Интернет кинотеатр


## Установить зависимости:

```bash
poetry install
```

Провести миграцию:

По умолчанию настроено на базу postgreSQL:
Измените натройки в файле

django_movie/settings.py (раздел DATABASES)


```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

Создать суперпользователя:

```bash
python manage.py createsuperuser
```

Загрузить данные из фикстуры(опционально):

```bash
manage.py loaddata data.json
```

Запустить веб-сервер проекта:

```bash
python manage.py runserver
```

