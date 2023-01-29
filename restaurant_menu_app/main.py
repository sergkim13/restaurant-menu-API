import http

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from restaurant_menu_app.database import SessionLocal

from . import crud, schemas
from .cache import clear_cache, get_cache, is_cached, set_cache

# from restaurant_menu_app.database import get_session


app = FastAPI(title='Restaurant menu')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def home():
    return 'Welcome to our restaurant!'


# Menu routers
@app.get(
    path='/api/v1/menus',
    response_model=list[schemas.MenuInfo],
    summary='Получение списка всех меню',
    status_code=http.HTTPStatus.OK,
)
def get_menus(db: Session = Depends(get_db)):
    if is_cached('menu', 'all'):
        return get_cache('menu', 'all')

    menus = crud.read_menus(db)
    set_cache('menu', 'all', menus)
    return menus


@app.get(
    path='/api/v1/menus/{menu_id}',
    response_model=schemas.MenuInfo,
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


@app.post(
    path='/api/v1/menus',
    response_model=schemas.MenuInfo,
    summary='Создание меню',
    status_code=http.HTTPStatus.CREATED,
)
def post_menu(new_menu: schemas.MenuCreate, db: Session = Depends(get_db)):

    try:
        menu = crud.create_menu(new_menu, db)
        set_cache('menu', menu.id, menu)
        clear_cache('menu', 'all')  # чистим кэш получения списка меню
        return menu

    except IntegrityError:
        raise HTTPException(
            status_code=400, detail='Menu with that title already exists.',
        )


@app.patch(
    path='/api/v1/menus/{menu_id}',
    response_model=schemas.MenuInfo,
    summary='Обновление меню',
    status_code=http.HTTPStatus.OK,
)
def patch_menu(menu_id: str, patch: schemas.MenuUpdate, db: Session = Depends(get_db)):

    if not crud.read_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='menu not found')

    crud.update_menu(menu_id, patch, db)
    updated_menu = crud.read_menu(menu_id, db)
    set_cache('menu', menu_id, updated_menu)
    clear_cache('menu', 'all')  # чистим кэш получения списка меню

    return updated_menu


@app.delete(
    path='/api/v1/menus/{menu_id}',
    response_model=schemas.Message,
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


# Submenu routers
@app.get(
    path='/api/v1/menus/{menu_id}/submenus',
    response_model=list[schemas.SubmenuInfo],
    summary='Просмотр списка подменю',
    status_code=http.HTTPStatus.OK,
)
def get_submenus(menu_id: str, db: Session = Depends(get_db)):
    if is_cached('submenu', 'all'):
        return get_cache('submenu', 'all')

    submenus = crud.read_submenus(menu_id, db)
    set_cache('submenu', 'all', submenus)
    return submenus


@app.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    response_model=schemas.SubmenuInfo,
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


@app.post(
    path='/api/v1/menus/{menu_id}/submenus',
    response_model=schemas.SubmenuInfo,
    summary='Создание подменю',
    status_code=http.HTTPStatus.CREATED,
)
def post_submenu(menu_id: str, new_submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
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


@app.patch(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    response_model=schemas.SubmenuInfo,
    summary='Обновление подменю',
    status_code=http.HTTPStatus.OK,
)
def patch_submenu(menu_id: str, submenu_id: str, patch: schemas.SubmenuUpdate, db: Session = Depends(get_db)):
    if not crud.read_submenu(menu_id, submenu_id, db):
        raise HTTPException(status_code=404, detail='submenu not found')

    crud.update_submenu(menu_id, submenu_id, patch, db)
    updated_submenu = crud.read_submenu(menu_id, submenu_id, db)

    set_cache('submenu', submenu_id, updated_submenu)
    # чистим кэш списка всех подменю, т.к. в одном подменю меняется содержимое
    clear_cache('submenu', 'all')

    return updated_submenu


@app.delete(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    response_model=schemas.Message,
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


# Dish routers
@app.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[schemas.DishInfo],
    summary='Просмотр списка блюд',
    status_code=http.HTTPStatus.OK,
)
def get_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    if is_cached('dish', 'all'):
        return get_cache('dish', 'all')

    dishes = crud.read_dishes(menu_id, submenu_id, db)
    set_cache('dish', 'all', dishes)
    return dishes


@app.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=schemas.DishInfo,
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


@app.post(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=schemas.DishInfo,
    summary='Создание блюда',
    status_code=http.HTTPStatus.CREATED,
)
def post_dish(menu_id: str, submenu_id: str, new_dish: schemas.DishCreate, db: Session = Depends(get_db)):
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
    # if crud.read_dish_by_title(menu_id, submenu_id, new_dish.title, db):
    #     raise HTTPException(
    #         status_code=400, detail='Dish with that title already exists.',
    #     )
    # return crud.create_dish(menu_id, submenu_id, new_dish, db)


@app.patch(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=schemas.DishInfo,
    summary='Обновление блюда',
    status_code=http.HTTPStatus.OK,
)
def patch_dish(menu_id: str, submenu_id: str, dish_id: str, patch: schemas.DishUpdate, db: Session = Depends(get_db)):
    if not crud.read_dish(menu_id, submenu_id, dish_id, db):
        raise HTTPException(status_code=404, detail='dish not found')

    crud.update_dish(submenu_id, dish_id, patch, db)
    updated_dish = crud.read_dish(menu_id, submenu_id, dish_id, db)

    set_cache('dish', dish_id, updated_dish)
    # чистим кэш списка всех блюд, т.к. в одном блюде меняется содержимое
    clear_cache('dish', 'all')

    return updated_dish


@app.delete(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=schemas.Message,
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


'_____________'

# @app.get('/')
# async def home():
#     return 'Welcome to our restaurant!'


# # Menu routers
# @app.get(
#     path='/api/v1/menus',
#     response_model=list[schemas.MenuInfo],
#     summary='Получение списка всех меню',
#     status_code=http.HTTPStatus.OK,
# )
# async def get_menus(db: Session = Depends(get_session)):
#     return await crud.read_menus(db)


# @app.get(
#     path='/api/v1/menus/{menu_id}',
#     response_model=schemas.MenuInfo,
#     summary='Получение информации о меню',
#     status_code=http.HTTPStatus.OK,
# )
# async def get_menu(menu_id: int, db: Session = Depends(get_session)):
#     menu = await crud.read_menu(menu_id, db)
#     if not menu:
#         raise HTTPException(status_code=404, detail='menu not found')
#     return menu


# @app.post(
#     path='/api/v1/menus',
#     response_model=schemas.MenuInfo,
#     summary='Создание меню',
#     status_code=http.HTTPStatus.CREATED,
# )
# async def post_menu(new_menu: schemas.MenuCreate, db: Session = Depends(get_session)):
#     if await crud.read_menu_by_title(new_menu.title, db):
#         raise HTTPException(
#             status_code=400, detail='Menu with that title already exists.',
#         )
#     else:
#         return await crud.create_menu(new_menu, db)


# @app.patch(
#     path='/api/v1/menus/{menu_id}',
#     response_model=schemas.MenuInfo,
#     summary='Обновление меню',
#     status_code=http.HTTPStatus.OK,
# )
# async def patch_menu(menu_id: str, patch: schemas.MenuUpdate, db: Session = Depends(get_session)):

#     if not await crud.read_menu(menu_id, db):
#         raise HTTPException(status_code=404, detail='menu not found')
#     await crud.update_menu(menu_id, patch, db)
#     return await crud.read_menu(menu_id, db)


# @app.delete(
#     path='/api/v1/menus/{menu_id}',
#     response_model=schemas.Message,
#     summary='Удаление меню',
#     status_code=http.HTTPStatus.OK,
# )
# async def delete_menu(menu_id: str, db: Session = Depends(get_session)):
#     if not await crud.read_menu(menu_id, db):
#         raise HTTPException(status_code=404, detail='menu not found')
#     await crud.delete_menu(menu_id, db)
#     message = {'status': True, 'message': 'The menu has been deleted'}
#     return message


# # Submenu routers
# @app.get(
#     path='/api/v1/menus/{menu_id}/submenus',
#     response_model=list[schemas.SubmenuInfo],
#     summary='Просмотр списка подменю',
#     status_code=http.HTTPStatus.OK,
# )
# async def get_submenus(menu_id: str, db: Session = Depends(get_session)):
#     return await crud.read_submenus(menu_id, db)


# @app.get(
#     path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
#     response_model=schemas.SubmenuInfo,
#     summary='Просмотр информации о подменю',
#     status_code=http.HTTPStatus.OK,
# )
# async def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_session)):
#     submenu = await crud.read_submenu(menu_id, submenu_id, db)
#     if not submenu:
#         raise HTTPException(status_code=404, detail='submenu not found')
#     return submenu


# @app.post(
#     path='/api/v1/menus/{menu_id}/submenus',
#     response_model=schemas.SubmenuInfo,
#     summary='Создание подменю',
#     status_code=http.HTTPStatus.CREATED,
# )
# async def post_submenu(menu_id: str, new_submenu: schemas.SubmenuCreate, db: Session = Depends(get_session)):
#     if await crud.read_submenu_by_title(menu_id, new_submenu.title, db):
#         raise HTTPException(
#             status_code=400, detail='Submenu with that title already exists.',
#         )
#     return await crud.create_submenu(menu_id, new_submenu, db)


# @app.patch(
#     path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
#     response_model=schemas.SubmenuInfo,
#     summary='Обновление подменю',
#     status_code=http.HTTPStatus.OK,
# )
# async def patch_submenu(menu_id: str, submenu_id: str, patch: schemas.SubmenuUpdate, db: Session = Depends(get_session)):
#     if not await crud.read_submenu(menu_id, submenu_id, db):
#         raise HTTPException(status_code=404, detail='submenu not found')
#     await crud.update_submenu(menu_id, submenu_id, patch, db)
#     return await crud.read_submenu(menu_id, submenu_id, db)


# @app.delete(
#     path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
#     response_model=schemas.Message,
#     summary='Удаление подменю',
#     status_code=http.HTTPStatus.OK,
# )
# async def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_session)):
#     if not await crud.read_submenu(menu_id, submenu_id, db):
#         raise HTTPException(status_code=404, detail='submenu not found')
#     await crud.delete_submenu(menu_id, submenu_id, db)
#     message = {'status': True, 'message': 'The submenu has been deleted'}
#     return message


# # Dish routers
# @app.get(
#     path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
#     response_model=list[schemas.DishInfo],
#     summary='Просмотр списка блюд',
#     status_code=http.HTTPStatus.OK,
# )
# async def get_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_session)):
#     return await crud.read_dishes(menu_id, submenu_id, db)


# @app.get(
#     path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
#     response_model=schemas.DishInfo,
#     summary='Просмотр информации о блюде',
#     status_code=http.HTTPStatus.OK,
# )
# async def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_session)):
#     dish = await crud.read_dish(menu_id, submenu_id, dish_id, db)
#     if not dish:
#         raise HTTPException(status_code=404, detail='dish not found')
#     return dish


# @app.post(
#     path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
#     response_model=schemas.DishInfo,
#     summary='Создание блюда',
#     status_code=http.HTTPStatus.CREATED,
# )
# async def post_dish(menu_id: str, submenu_id: str, new_dish: schemas.DishCreate, db: Session = Depends(get_session)):
#     if await crud.read_dish_by_title(menu_id, submenu_id, new_dish.title, db):
#         raise HTTPException(
#             status_code=400, detail='Dish with that title already exists.',
#         )
#     return await crud.create_dish(menu_id, submenu_id, new_dish, db)


# @app.patch(
#     path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
#     response_model=schemas.DishInfo,
#     summary='Обновление блюда',
#     status_code=http.HTTPStatus.OK,
# )
# async def patch_dish(menu_id: str, submenu_id: str, dish_id: str, patch: schemas.DishUpdate, db: Session = Depends(get_session)):
#     if not await crud.read_dish(menu_id, submenu_id, dish_id, db):
#         raise HTTPException(status_code=404, detail='dish not found')

#     await crud.update_dish(submenu_id, dish_id, patch, db)
#     return await crud.read_dish(menu_id, submenu_id, dish_id, db)


# @app.delete(
#     path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
#     response_model=schemas.Message,
#     summary='Удаление блюда',
#     status_code=http.HTTPStatus.OK,
# )
# async def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_session)):
#     if not await crud.read_dish(menu_id, submenu_id, dish_id, db):
#         raise HTTPException(status_code=404, detail='dish not found')
#     await crud.delete_dish(submenu_id, dish_id, db)
#     message = {'status': True, 'message': 'The dish has been deleted'}
#     return message
