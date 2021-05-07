# avia_search

## Работа с проектом
# Надо запустить postgres server
## Создать базу данных с данными файла настроек
```
DB_NAME=transavia
DATABASE_SCHEMA=public
DB_USER=transavia
DB_PASSWORD=transavia
DB_HOST=localhost
DB_PORT=5432
```
# Запуск виртуального окружения
```
python3 -m venv env
source env/bin/activate
```
# Установка библиотек
```
pip install -r requirements.txt
```
# Запуск миграции
```
python manage.py migrate
```
# Открыть shell plus и запуск скриптов для вытягивания дааных с источников
```
python manage.py shell_plus
from app.core.parsers import get_core_data
get_core_data()
```
# Запуск проекта и создание запросов в swagger  http://127.0.0.1:8000/swagger/
```
python manage.py runserver
```
