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
from restaurant_menu_app.schemas.scheme import (
    Message,
    SubmenuCreate,
    SubmenuInfo,
    SubmenuUpdate,
)


class SubmenuService():
    def __init__(self, db: Session):
        self.db = db

    def get_list(self, menu_id: str) -> list[SubmenuInfo]:
        '''Получить список подменю.'''

        if is_cached('submenu', 'all'):
            return get_cache('submenu', 'all')

        submenus = crud.read_submenus(menu_id, self.db)
        set_cache('submenu', 'all', submenus)
        return submenus

    def get_info(self, menu_id: str, submenu_id: str) -> SubmenuInfo:
        '''Получить информацию о подменю.'''

        if is_cached('submenu', submenu_id):
            return get_cache('submenu', submenu_id)

        submenu = crud.read_submenu(menu_id, submenu_id, self.db)
        if not submenu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='submenu not found',
            )
        set_cache('submenu', submenu_id, submenu)
        return submenu

    def create(self, menu_id: str, data: SubmenuCreate) -> SubmenuInfo:
        '''Создать подменю.'''

        try:
            new_submenu_id = crud.create_submenu(menu_id, data, self.db)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, detail='Submenu with that title already exists',
                )
            elif isinstance(e.orig, ForeignKeyViolation):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, detail='parent menu not found',
                )
            else:
                raise

        new_submenu = crud.read_submenu(menu_id, new_submenu_id, self.db)
        set_cache('submenu', new_submenu_id, new_submenu)
        # Чистим кэш для родительских элементов и получения списков элементов
        clear_cache('submenu', 'all')
        clear_cache('menu', menu_id)
        clear_cache('menu', 'all')
        return new_submenu

    def update(self, menu_id: str, submenu_id: str, patch: SubmenuUpdate) -> SubmenuInfo:
        '''Обновить подменю.'''

        if not crud.read_submenu(menu_id, submenu_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='submenu not found',
            )

        crud.update_submenu(menu_id, submenu_id, patch, self.db)
        updated_submenu = crud.read_submenu(menu_id, submenu_id, self.db)
        set_cache('submenu', submenu_id, updated_submenu)
        clear_cache('submenu', 'all')  # чистим кэш получения списка подменю
        return updated_submenu

    def delete(self, menu_id: str, submenu_id: str) -> Message:
        '''Удалить подменю.'''

        if not crud.read_submenu(menu_id, submenu_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='submenu not found',
            )

        crud.delete_submenu(menu_id, submenu_id, self.db)
        clear_cache('submenu', submenu_id)
        # Чистим кэш для родительских элементов и получения списков элементов
        clear_cache('submenu', 'all')
        clear_cache('menu', menu_id)
        clear_cache('menu', 'all')
        return Message(status=True, message='The submenu has been deleted')


def get_submenu_service(db: Session = Depends(get_db)) -> SubmenuService:
    return SubmenuService(db=db)
