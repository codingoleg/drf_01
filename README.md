# Django Rest Api

Демонстрация использования:
https://youtu.be/j5qVfiWHFfU

## Installation
+ Клонируйте репозиторий:
```bash
git clone https://github.com/codingoleg/drf_01.git
```
+ Перейдите в него:
```bash
cd .\drf_01\drf_01\
```
+ Установите зависимости:
```bash
pip install -r requirements.txt
```
+ Отредактируйте при необходимости .\django_core\settings.py.
В проекте используется postgresql через Django ORM. \
Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```
+ Запустите сервер:
```bash
python manage.py runserver
```

## License
GNU GPLv3 