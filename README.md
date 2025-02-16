# Тестовое задание для Backend разработчика (junior)

## Описание
Сервис, который принимает запрос с указанием кадастрового номера, широты и долготы, эмулирует 
отправку запроса на внешний сервер, который может обрабатывать запрос до 60 секунд. Затем должен отдавать результат запроса. Считается, что внешний сервер может ответить `true` или `false`.

Пользователям доступа регистрация(JWT токен), авторизация, просмотр своего профиля и смена пароля.

Реализована [админ-панель](http://127.0.0.1:8000/admin/login) для просмотра пользователей, ролей и гео запросов. Админ создается при первом
запуске сервиса, по умолчанию данные указаны в переменных окружения. Пример лежит в корне проекта 
в файле `example.env`

Реализован отдельный сервис для эмуляции запросов на сервер. Принимает запросы с основного:   
`POST /api/v1/query` - принимает запрос с указанием кадастрового номера, широты и долготы и 
отправляет на внешний сервер. Отвечает с задержкой у казанной в параметре `DELAY` в файле `.env`  
`GET /api/v1/ping` - проверка, что моковый сервер доступен

Примеры ендпоинтов можно посмотреть в [Swagger](http://127.0.0.1:8000/docs), там же есть описание 
валидаций по некоторым ендпоинтам.


<details><summary>Задание</summary>
<br>

### Тестовое задание для Backend разработчика (junior)  
#### Описание задания:  
Написать сервис, который принимает запрос с указанием кадастрового номера, широты и долготы, эмулирует отправку запроса на внешний сервер, который может обрабатывать запрос до 60 секунд. Затем должен отдавать результат запроса. Считается, что внешний сервер может ответить `true` или `false`.
Данные запроса на сервер и ответ с внешнего сервера должны быть сохранены в БД. Нужно написать 
АПИ для получения истории всех запросов/истории по кадастровому номеру.  
#### Сервис должен содержать следующие эндпоинты:  
"/query" - принимает кадастровый номер  
"/ping" - проверка, что  сервер запустился  
"/history" - для получения истории запросов  
"/result" - эндпоинт эмулируемоего сервера, который возвращает `true` или `false`  
Сервис завернуть в Dockerfile.  
Составить README с запуском. Наставникам будет проще и быстрее проверить вашу работу.  
#### Необходимый стэк:  
FastAPI (async роуты)
PostgreSQL
SQLAlchemy (async запросы)
Alembic
Docker
Docker Compose
Pytest  
#### Дополнительные требования:
*Дополнительное задание №1. Можно добавить дополнительный сервис, который будет принимать 
запросы первого сервиса и эмулировать внешний сервер.  
*Дополнительное задание №2. Можно добавить регистрацию и авторизацию


Будет плюсом!
Документация к сервису
Тесты функционала
Валидация данных
Админ Панель


</details>

## Инструкция по установке

- Клонируйте репозиторий командой:
```bash
git clone git@github.com:AndreyKilanov/test_task_antipoff.git
```
  

- Запустите контейнеры командой:
```bash
docker-compose up -d --build
```
- После запуска проекта Swagger будет доступен по [адресу](http://127.0.0.1:8000/docs)

## Стек

1. [x] fastapi 0.115.8
2. [x] SQLAlchemy 2.0.38
3. [x] alembic 1.14.1
4. [x] asyncpg 0.30.0
5. [x] httpx 0.28.1
6. [x] pyjwt 2.10.1
7. [x] passlib[bcrypt] 1.7.4
8. [x] sqladmin[full] 0.20.1


## Контакты
[![](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/AndyFebruary)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AndreyKilanov)
