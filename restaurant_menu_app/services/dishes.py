from http import HTTPStatus

from fastapi import Depends, HTTPException
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from restaurant_menu_app.db.cache.cache_utils import (
    clear_cache,
    get_cache,
    is_cached,
    set_cache,
)
from restaurant_menu_app.db.main_db import crud
from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.schemas.scheme import DishCreate, DishInfo, DishUpdate, Message


class DishService():
    def __init__(self, db: Session):
        self.db = db

    def get_list(self, menu_id: str, submenu_id: str) -> list[DishInfo]:
        '''Получить список блюд.'''

        if is_cached('dish', 'all'):
            return get_cache('dish', 'all')

        dishes = crud.read_dishes(menu_id, submenu_id, self.db)
        set_cache('dish', 'all', dishes)
        return dishes

    def get_info(self, menu_id: str, submenu_id: str, dish_id: str) -> DishInfo:
        '''Полчить информациб о блюде.'''

        if is_cached('dish', dish_id):
            return get_cache('dish', dish_id)

        dish = crud.read_dish(menu_id, submenu_id, dish_id, self.db)
        if not dish:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='dish not found',
            )
        set_cache('dish', dish_id, dish)
        return dish

    def create(self, menu_id: str, submenu_id: str, data: DishCreate) -> DishInfo:
        '''Создать блюдо.'''

        try:
            new_dish = crud.create_dish(submenu_id, data, self.db)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, detail='Dish with that title already exists',
                )
            elif isinstance(e.orig, ForeignKeyViolation):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, detail='parent submenu not found',
                )
            else:
                raise

        created_dish = crud.read_dish(
            menu_id, submenu_id, new_dish.id, self.db,
        )
        set_cache('dish', new_dish.id, created_dish)
        # Чистим кэш для родительских элементов и получения списков элементов
        clear_cache('dish', 'all')
        clear_cache('submenu', submenu_id)
        clear_cache('submenu', 'all')
        clear_cache('menu', menu_id)
        clear_cache('menu', 'all')
        return created_dish

    def update(self, menu_id: str, submenu_id: str, dish_id: str, patch: DishUpdate) -> DishInfo:
        '''Обновить блюдо.'''

        if not crud.read_dish(menu_id, submenu_id, dish_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='dish not found',
            )

        crud.update_dish(menu_id, submenu_id, dish_id, patch, self.db)
        updated_dish = crud.read_dish(menu_id, submenu_id, dish_id, self.db)
        set_cache('dish', dish_id, updated_dish)
        clear_cache('dish', 'all')  # чистим кэш получения списка блюд
        return updated_dish

    def delete(self, menu_id: str, submenu_id: str, dish_id: str) -> Message:
        '''Удалить блюдо.'''

        if not crud.read_dish(menu_id, submenu_id, dish_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='dish not found',
            )

        crud.delete_dish(submenu_id, dish_id, self.db)
        clear_cache('dish', dish_id)
        # Чистим кэш для родительских элементов и получения списков элементов
        clear_cache('dish', 'all')
        clear_cache('submenu', submenu_id)
        clear_cache('submenu', 'all')
        clear_cache('menu', menu_id)
        clear_cache('menu', 'all')
        return Message(status=True, message='The dish has been deleted')


def get_dish_service(db: Session = Depends(get_db)) -> DishService:
    return DishService(db=db)
