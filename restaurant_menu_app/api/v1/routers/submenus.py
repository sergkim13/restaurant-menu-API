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
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['Submenus'],
)


@router.get(
    path='',
    response_model=list[scheme.SubmenuInfo],
    summary='Просмотр списка подменю',
    status_code=http.HTTPStatus.OK,
)
def get_submenus(menu_id: str, db: Session = Depends(get_db)):
    if is_cached('submenu', 'all'):
        return get_cache('submenu', 'all')

    submenus = crud.read_submenus(menu_id, db)
    set_cache('submenu', 'all', submenus)
    return submenus


@router.get(
    path='/{submenu_id}',
    response_model=scheme.SubmenuInfo,
    summary='Просмотр информации о подменю',
    status_code=http.HTTPStatus.OK,
)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    if is_cached('submenu', submenu_id):
        return get_cache('submenu', submenu_id)

    submenu = crud.read_submenu(menu_id, submenu_id, db)

    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    set_cache('submenu', submenu_id, submenu)
    return submenu


@router.post(
    path='',
    response_model=scheme.SubmenuInfo,
    summary='Создание подменю',
    status_code=http.HTTPStatus.CREATED,
)
def post_submenu(menu_id: str, new_submenu: scheme.SubmenuCreate, db: Session = Depends(get_db)):
    try:
        submenu = crud.create_submenu(menu_id, new_submenu, db)
        set_cache('submenu', submenu.id, submenu)

        # Чистим кэш для родительских элементов и получения списков элементов
        clear_cache('submenu', 'all')
        clear_cache('menu', menu_id)
        clear_cache('menu', 'all')

        return submenu

    except IntegrityError:
        raise HTTPException(
            status_code=400, detail='Submenu with that title already exists.',
        )


@router.patch(
    path='/{submenu_id}',
    response_model=scheme.SubmenuInfo,
    summary='Обновление подменю',
    status_code=http.HTTPStatus.OK,
)
def patch_submenu(menu_id: str, submenu_id: str, patch: scheme.SubmenuUpdate, db: Session = Depends(get_db)):
    if not crud.read_submenu(menu_id, submenu_id, db):
        raise HTTPException(status_code=404, detail='submenu not found')

    crud.update_submenu(menu_id, submenu_id, patch, db)
    updated_submenu = crud.read_submenu(menu_id, submenu_id, db)

    set_cache('submenu', submenu_id, updated_submenu)
    # чистим кэш списка всех подменю, т.к. в одном подменю меняется содержимое
    clear_cache('submenu', 'all')

    return updated_submenu


@router.delete(
    path='/{submenu_id}',
    response_model=scheme.Message,
    summary='Удаление подменю',
    status_code=http.HTTPStatus.OK,
)
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    if not crud.read_submenu(menu_id, submenu_id, db):
        raise HTTPException(status_code=404, detail='submenu not found')
    crud.delete_submenu(menu_id, submenu_id, db)
    clear_cache('submenu', submenu_id)

    # Чистим кэш для родительских элементов и получения списков элементов
    clear_cache('submenu', 'all')
    clear_cache('menu', menu_id)
    clear_cache('menu', 'all')

    message = {'status': True, 'message': 'The submenu has been deleted'}
    return message
