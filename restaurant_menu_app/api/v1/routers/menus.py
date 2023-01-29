import http

from fastapi import APIRouter, Depends, HTTPException
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
from restaurant_menu_app.schemas import scheme

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['Menus'],
)


@router.get(
    path='',
    response_model=list[scheme.MenuInfo],
    summary='Получение списка всех меню',
    status_code=http.HTTPStatus.OK,
)
def get_menus(db: Session = Depends(get_db)):
    if is_cached('menu', 'all'):
        return get_cache('menu', 'all')

    menus = crud.read_menus(db)
    set_cache('menu', 'all', menus)
    return menus


@router.get(
    path='/{menu_id}',
    response_model=scheme.MenuInfo,
    summary='Получение информации о меню',
    status_code=http.HTTPStatus.OK,
)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    if is_cached('menu', menu_id):
        return get_cache('menu', menu_id)

    menu = crud.read_menu(menu_id, db)

    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')

    set_cache('menu', menu_id, menu)
    return menu


@router.post(
    path='',
    response_model=scheme.MenuInfo,
    summary='Создание меню',
    status_code=http.HTTPStatus.CREATED,
)
def post_menu(new_menu: scheme.MenuCreate, db: Session = Depends(get_db)):

    try:
        menu = crud.create_menu(new_menu, db)
        set_cache('menu', menu.id, menu)
        clear_cache('menu', 'all')  # чистим кэш получения списка меню
        return menu

    except IntegrityError:
        raise HTTPException(
            status_code=400, detail='Menu with that title already exists.',
        )


@router.patch(
    path='/{menu_id}',
    response_model=scheme.MenuInfo,
    summary='Обновление меню',
    status_code=http.HTTPStatus.OK,
)
def patch_menu(menu_id: str, patch: scheme.MenuUpdate, db: Session = Depends(get_db)):

    if not crud.read_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='menu not found')

    crud.update_menu(menu_id, patch, db)
    updated_menu = crud.read_menu(menu_id, db)
    set_cache('menu', menu_id, updated_menu)
    clear_cache('menu', 'all')  # чистим кэш получения списка меню

    return updated_menu


@router.delete(
    path='/{menu_id}',
    response_model=scheme.Message,
    summary='Удаление меню',
    status_code=http.HTTPStatus.OK,
)
def delete_menu(menu_id: str, db: Session = Depends(get_db)):

    if not crud.read_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='menu not found')

    crud.delete_menu(menu_id, db)
    clear_cache('menu', menu_id)
    clear_cache('menu', 'all')  # чистим кэш получения списка меню
    message = {'status': True, 'message': 'The menu has been deleted'}
    return message
