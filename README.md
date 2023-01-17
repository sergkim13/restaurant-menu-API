# Restaurant menu API (FastApi)

[![Maintainability](https://api.codeclimate.com/v1/badges/88f08c3ce1a9a1d195c5/maintainability)](https://codeclimate.com/github/sergkim13/restaurant_menu_API-FastAPI/maintainability)

### Description:
Restaurant menu API allows you to get information about menus, submenus and dishes. See "Task description" section below for more.
Made with FastAPI, PostgreSQL, SQLAlchemy, pydantic, alembic.

### Requirements:
1. MacOS / Linux
2. Poetry

### Install:
1. Clone repository: `https://github.com/sergkim13/ylab_project.git`
2. Type `make install` for installing required dependencies by Poetry
3. Type `make prepare-migrations` for preparing alembic migrations
4. Move `env.py ` from project root to migrations dir, created in step 3, with replacement 
5. Fill in `.env` with your local PostgreSQL DB name, DB username and DB password
6. Type `make migrations` for creating tables
7. Type `make start` for application startup

__________

### Task description (stage №1).

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
  