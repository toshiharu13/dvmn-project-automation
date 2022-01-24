# Запись на время конференций проекта, создание команд по полученному времени. 
Телеграм-бот на основе python-telegram-bot и Django.

[![Python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)
## Описание
*Проект не закончен.*

Программа с помощью телеграм бота проводит опрос студентов удобного времени будующих конференций в рамках проекта.
После сбора данных, программа формирует команды для предстоящего проекта.

## Как установить
 - Склонировать проект
```shell
git clone https://github.com/delphython/dvmn-project-automation.git
```
 - Установить requirements.txt
```shell
pip install -r requirements.txt
```
 - Создать файл .env и заполнить в нем переменные:
 
```dotenv
TG_TOKEN = 'токен бота'
```
```dotenv
STUDENTS_JSON = 'имя файла для импорта данных о студентах в БД(по умолчанию students.json)'
```
```dotenv
PM_JSON = 'имя файла для импорта данных о проджект менеджерах(ПМ) в БД(по умолчанию pm.json)'
```
## Перед первым запуском бота:
 - Сделать миграцию
```shell
python manage.py migrate
```
 - Скачать в корень проекта файлы для импорта данных студентов и ПМ, убедиться что они названы по умолчанию, либо ввести названия в файл .env(см. выше).

 - Импортировать данные о студентах:
```shell
python manage.py dumpload -s
```
 - импортировать данные о ПМ:
```shell
python manage.py dumpload -p
```

## Запустить бота:
```shell
python manage.py bot
```
## запуск админки:
 - запустить сервер Django
 - пройти в адмнку
```
<адрес запущенного сервера>/admin
```

## Цель проекта
Код написан в рамках самостоятельного проекта на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org).