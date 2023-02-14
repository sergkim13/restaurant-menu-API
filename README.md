# Restaurant menu API (FastApi)

[![Maintainability](https://api.codeclimate.com/v1/badges/88f08c3ce1a9a1d195c5/maintainability)](https://codeclimate.com/github/sergkim13/restaurant_menu_API-FastAPI/maintainability)

### Description:
Restaurant menu API allows you to get information about menus, submenus and dishes. See "Task description" section below for more.
Made with:
- FastAPI,
- PostgreSQL,
- SQLAlchemy,
- Pydantic,
- Alembic,
- Docker,
- Redis,
- Celery,
- RabbitMQ.

### Requirements:
1. MacOS (prefer) / Linux / Windows10
2. `Docker`
3. `Make` utily for MacOS, Linux.

### Install:
1. Clone repository: `https://github.com/sergkim13/restaurant_menu_FastAPI.git`
2. Type `make compose` for running application in docker container. App will be running at http://0.0.0.0:8000. Type `make stop` to stop app container.
3. Type `make compose-test` for running tests in docker container. Type `make stop-test` to stop app container.
4. For checking `pre-commit hooks` you need `Poetry` and install dependencies:
    - `make install`
    - `make hooks`
5. To generate test data:
`POST http://0.0.0.0:8000/api/v1/generated_test_data`
6. To create xlsx-file with all data:
`POST http://0.0.0.0:8000/api/v1/content_as_file`
You will get `task_id` as a response.
7. To download xlsx-file with all data:
`GET http://0.0.0.0:8000/api/v1/content_as_file/{task_id}`

Pre-commit hooks demo:
[![asciicast](https://asciinema.org/a/UoPQrqTPphCQbaCHselI5VPYU.svg)](https://asciinema.org/a/UoPQrqTPphCQbaCHselI5VPYU)


### **Task description**
<details open>
    <summary>Click to show</summary>

### **Task description (stage №4)** - ✅
В этом домашнем задании надо:
1. Переписать текущее FastAPI приложение на асинхронное выполнение.
2. Добавить в проект фоновую задачу с помощью Celery + RabbitMQ.
Фоновая задача по генераций меню нашего ресторана в виде excel-документа.
Для этого пункта понадобится добавить 2 ендпоинта:
- (POST) для запуска фоновой задачи для генераций excel-файла
- (GET) для получения результата задачи в виде ссылки на скачивание excel-файла
3. Отдельный ендпоинт который заполнит базу тестовыми данными, для последующего генераций меню в excel-файл

Требования:
- Данные меню, подменю, блюд для генераций excel-файла, должны доставаться одним ORM-запросом в БД (использовать подзапросы и агрегирующие функций SQL).
- Код должен проходить все линтеры (black, autopep, flake8, mypy, isort). Файл с pre-commit хуками будет приложен к презентаций.
- Проект должен соответствовать требованиям в предыдущих вебинарах.



__________
### **Task description (stage №3)** - ✅.
В этом домашнем задании надо:
1. Вынести бизнес логику и запросы в БД в отдельные слои приложения.
2. Добавить кэш хранилище Redis
3. Добавить pre-commit хуки в проект
4. Описать ручки API в соответствий c OpenAPI

Требования:
- Код должен проходить все линтеры.
- Код должен соответствовать принципам SOLID, DRY, KISS.
- Проект должен запускаться по одной команде.
- Проект должен проходить все Postman тесты (коллекция с Вебинара №1).
- Тесты написанные вами после Вебинара №2, должны быть актуальны, запускать и успешно проходить

Дополнительно:
- Проект запускается по одной команде
- Тесты запускаются по другой


__________
### **Task description (stage №2)** - ✅.
В этом домашнем задании надо написать тесты для ранее разработанных ендпоинтов вашего API после вебинара №1.
А именно:
1. Обернуть программные компоненты в контейнеры. Контейнеры должны запускаться по одной команде `docker-compose up -d` или той которая описана вами в readme.md.
Образы для Docker:
- (API) python:3.10-slim
- (DB) 	postgres:15.1-alpine

2. Написать CRUD тесты для ранее разработанного API с помощью библиотеки pytest
3. Подготовить отдельный контейнер для запуска тестов

Если FastAPI синхронное - тесты синхронные,
Иначе FastAPI асинхронное - тесты асинхронные

__________

### **Task description (stage №1)** - ✅.

Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции. Для проверки задания, к презентаций будет приложена Postman коллекция с тестами. Задание выполнено, если все тесты проходят успешно.

Даны 3 сущности: Меню, Подменю, Блюдо.

Зависимости:
- меню есть подменю, которые к ней привязаны.
- подменю есть блюда.

Условия:
- Блюдо не может быть привязано напрямую к меню, минуя подменю.
- Блюдо не может находиться в 2-х подменю одновременно.
- Подменю не может находиться в 2-х меню одновременно.
- Если удалить меню, должны удалиться все подменю и блюда этого меню.
- Если удалить подменю, должны удалиться все блюда этого подменю.
- Цены блюд выводить с округлением до 2 знаков после запятой.
- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.
- Во время запуска тестового сценария БД должна быть пуста.
</details>
