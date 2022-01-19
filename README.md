## Описание

Телеграм-бот на основе python-telegram-bot и Django.

Создать файл .env в корне каталога с проектом и прописать: 
```dotenv
TG_TOKEN = 'токен бота'
```
```dotenv
STUDENTS_JSON = 'имя файла для импорта данных о студентах в БД(по умолчанию students.json)'
```
```dotenv
PM_JSON = 'имя файла для импорта данных о проджект менеджерах в БД(по умолчанию pm.json)'
```
До запуска бота:
```shell
python manage.py migrate
```


Запустить бота:
```shell
python manage.py bot
```

