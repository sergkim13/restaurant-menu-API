from http import HTTPStatus

from fastapi import Depends, HTTPException
from psycopg2.errors import UniqueViolation
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
from restaurant_menu_app.schemas.scheme import MenuCreate, MenuInfo, MenuUpdate, Message


class MenuService():
    def __init__(self, db: Session):
        self.db = db

    def get_list(self) -> list[MenuInfo]:
        '''Получить список меню.'''

        if is_cached('menu', 'all'):
            return get_cache('menu', 'all')

        menus = crud.read_menus(self.db)
        set_cache('menu', 'all', menus)
        return menus

    def get_info(self, menu_id: str) -> MenuInfo:
        '''Получить информацию о меню.'''

        if is_cached('menu', menu_id):
            return get_cache('menu', menu_id)

        menu = crud.read_menu(menu_id, self.db)
        if not menu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='menu not found',
            )
        set_cache('menu', menu_id, menu)
        return menu

    def create(self, data: MenuCreate) -> MenuInfo:
        '''Cоздать меню.'''

        try:
            new_menu = crud.create_menu(data, self.db)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, detail='Menu with that title already exists',
                )
            else:
                raise

        created_menu = crud.read_menu(new_menu.id, self.db)
        set_cache('menu', new_menu.id, created_menu)
        clear_cache('menu', 'all')  # чистим кэш получения списка меню
        return created_menu

    def update(self, menu_id: str, patch: MenuUpdate) -> MenuInfo:
        '''Обновить меню.'''

        if not crud.read_menu(menu_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='menu not found',
            )

        crud.update_menu(menu_id, patch, self.db)
        updated_menu = crud.read_menu(menu_id, self.db)
        set_cache('menu', menu_id, updated_menu)
        clear_cache('menu', 'all')  # чистим кэш получения списка меню
        return updated_menu

    def delete(self, menu_id: str) -> Message:
        '''Удалить меню.'''

        if not crud.read_menu(menu_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='menu not found',
            )

        crud.delete_menu(menu_id, self.db)
        clear_cache('menu', menu_id)
        clear_cache('menu', 'all')  # чистим кэш получения списка меню
        return Message(status=True, message='The menu has been deleted')


def get_menu_service(db: Session = Depends(get_db)) -> MenuService:
    return MenuService(db=db)
