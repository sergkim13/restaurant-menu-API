from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from restaurant_menu_app.database import SessionLocal, engine
from .database import Base
from . import schemas, crud 

Base.metadata.create_all(bind=engine)

app = FastAPI()


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
@app.get('/api/v1/menus', response_model=List[schemas.MenuInfo])
def get_menus(db: Session = Depends(get_db)):
    menus = crud.read_menus(db)
    return menus


@app.get('/api/v1/menus/{menu_id}', response_model=schemas.MenuInfo)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = crud.read_menu(menu_id, db)
    if not menu:
        raise HTTPException(status_code=404, detail='Menu not found.')
    return menu


@app.post('/api/v1/menus', response_model=schemas.MenuInfo)
def post_menu(new_menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    if crud.read_menu_by_title(new_menu.title, db):
        raise HTTPException(status_code=400, detail="Menu with that title already exists.")
    return crud.create_menu(new_menu, db)


@app.patch('/api/v1/menus/{menu_id}', response_model=schemas.MenuInfo)
def patch_menu(menu_id: str, patch: schemas.MenuUpdate, db: Session = Depends(get_db)):
    if not crud.read_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='Menu not found.')
    updated_menu = crud.update_menu(menu_id, patch, db)
    return updated_menu


@app.delete('/app/v1/menus/{menu_id}', response_model=schemas.Message)
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    if not crud.read_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='Menu not found.')
    result = crud.delete_menu(menu_id, db)
    return result


# Submenu routers
@app.get('/api/v1/menus/{menu_id}/submenus', response_model=List[schemas.SubmenuInfo])
def get_submenus(menu_id: str, db: Session = Depends(get_db)):
    submenus = crud.read_submenus(menu_id, db)
    return submenus


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubmenuInfo)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    submenu = crud.read_submenu(menu_id, submenu_id, db)
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@app.post('/api/v1/menus/{menu_id}/submenus', response_model=schemas.SubmenuInfo)
def post_submenu(menu_id: str, new_submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    if crud.read_submenu_by_title(menu_id, new_submenu.title, db):
        raise HTTPException(status_code=400, detail="Submenu with that title already exists.")
    return crud.create_submenu(menu_id, new_submenu, db)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubmenuInfo)
def patch_submenu(menu_id: str, submenu_id: str, patch: schemas.MenuUpdate, db: Session = Depends(get_db)):
    if not crud.read_submenu(menu_id, submenu_id, db):
        raise HTTPException(status_code=404, detail='submenu not found')
    updated_submenu = crud.update_submenu(menu_id, submenu_id, patch, db)
    return updated_submenu


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.Message)
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    if not crud.read_submenu(menu_id, submenu_id, db):
        raise HTTPException(status_code=404, detail='Submenu not found.')
    result = crud.delete_submenu(menu_id, submenu_id, db)
    return result


# Dish routers
@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=List[schemas.DishInfo])
def get_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    dishes = crud.read_dishes(menu_id, submenu_id, db)
    return dishes


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.DishInfo)
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return crud.read_dish(menu_id, submenu_id, dish_id, db)


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=schemas.DishInfo)
def post_dish(menu_id: str, submenu_id: str, new_dish: schemas.DishCreate, db: Session = Depends(get_db)):
    if crud.read_dish_by_title(menu_id, submenu_id, new_dish.title, db):
        raise HTTPException(status_code=400, detail="Dish with that title already exists.")
    return crud.create_dish(submenu_id, new_dish, db)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.DishInfo)
def patch_dish(menu_id: str, submenu_id: str, dish_id: str, patch: schemas.DishUpdate, db: Session = Depends(get_db)):
    if not crud.read_dish(menu_id, submenu_id, dish_id, db):
        raise HTTPException(status_code=404, detail='Dish not found')
    updated_dish = crud.update_dish(menu_id, submenu_id, dish_id, patch, db)
    return updated_dish


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Message)
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    if not crud.read_dish(menu_id, submenu_id, dish_id, db):
        raise HTTPException(status_code=404, detail='Dish not found')
    result = crud.delete_dish(submenu_id, dish_id, db)
    return result
