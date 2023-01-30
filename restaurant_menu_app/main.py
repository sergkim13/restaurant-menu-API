from fastapi import FastAPI

from restaurant_menu_app.api.v1.routers.dishes import router as dish_router
from restaurant_menu_app.api.v1.routers.menus import router as menus_router
from restaurant_menu_app.api.v1.routers.submenus import router as submenu_router

app = FastAPI(
    title='Restaurant menu',
    description='Restaurant menu API, powered by FastAPI',
    version='0.1.0',
)
app.include_router(menus_router)
app.include_router(submenu_router)
app.include_router(dish_router)


@app.get(
    path='/',
    summary='Домашняя страница',
    tags=['Home'],
)
def home():
    return 'Welcome to our restaurant!'
