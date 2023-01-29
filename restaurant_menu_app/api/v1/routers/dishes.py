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
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dishes'],
)


@router.get(
    path='',
    response_model=list[scheme.DishInfo],
    summary='Просмотр списка блюд',
    status_code=http.HTTPStatus.OK,
)
def get_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    if is_cached('dish', 'all'):
        return get_cache('dish', 'all')

    dishes = crud.read_dishes(menu_id, submenu_id, db)
    set_cache('dish', 'all', dishes)
    return dishes


@router.get(
    path='/{dish_id}',
    response_model=scheme.DishInfo,
    summary='Просмотр информации о блюде',
    status_code=http.HTTPStatus.OK,
)
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):

    if is_cached('dish', dish_id):
        return get_cache('dish', dish_id)

    dish = crud.read_dish(menu_id, submenu_id, dish_id, db)
    if not dish:
        raise HTTPException(status_code=404, detail='dish not found')

    set_cache('dish', dish_id, dish)
    return dish


@router.post(
    path='',
    response_model=scheme.DishInfo,
    summary='Создание блюда',
    status_code=http.HTTPStatus.CREATED,
)
def post_dish(menu_id: str, submenu_id: str, new_dish: scheme.DishCreate, db: Session = Depends(get_db)):
    try:
        dish = crud.create_dish(menu_id, submenu_id, new_dish, db)
        set_cache('dish', dish.id, dish)

        # Чистим кэш для родительских элементов и получения списков элементов
        clear_cache('dish', 'all')
        clear_cache('submenu', submenu_id)
        clear_cache('submenu', 'all')
        clear_cache('menu', menu_id)
        clear_cache('menu', 'all')

        return dish
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail='Dish with that title already exists.',
        )


@router.patch(
    path='/{dish_id}',
    response_model=scheme.DishInfo,
    summary='Обновление блюда',
    status_code=http.HTTPStatus.OK,
)
def patch_dish(menu_id: str, submenu_id: str, dish_id: str, patch: scheme.DishUpdate, db: Session = Depends(get_db)):
    if not crud.read_dish(menu_id, submenu_id, dish_id, db):
        raise HTTPException(status_code=404, detail='dish not found')

    crud.update_dish(submenu_id, dish_id, patch, db)
    updated_dish = crud.read_dish(menu_id, submenu_id, dish_id, db)

    set_cache('dish', dish_id, updated_dish)
    # чистим кэш списка всех блюд, т.к. в одном блюде меняется содержимое
    clear_cache('dish', 'all')

    return updated_dish


@router.delete(
    path='/{dish_id}',
    response_model=scheme.Message,
    summary='Удаление блюда',
    status_code=http.HTTPStatus.OK,
)
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    if not crud.read_dish(menu_id, submenu_id, dish_id, db):
        raise HTTPException(status_code=404, detail='dish not found')
    crud.delete_dish(submenu_id, dish_id, db)
    clear_cache('dish', dish_id)

    # Чистим кэш для родительских элементов и получения списков элементов
    clear_cache('dish', 'all')
    clear_cache('submenu', submenu_id)
    clear_cache('submenu', 'all')
    clear_cache('menu', menu_id)
    clear_cache('menu', 'all')

    message = {'status': True, 'message': 'The dish has been deleted'}
    return message
