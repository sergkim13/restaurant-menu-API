from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from restaurant_menu_app.database import SessionLocal  #, engine
# from .database import Base
from . import schemas, crud

# Base.metadata.create_all(bind=engine)

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
@app.get('/api/v1/menus', response_model=List[schemas.MenuInfo])
def get_menus(db: Session = Depends(get_db)):
    return crud.read_menus(db)


@app.get('/api/v1/menus/{menu_id}', response_model=schemas.MenuInfo)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = crud.read_menu(menu_id, db)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@app.post('/api/v1/menus', response_model=schemas.MenuInfo, status_code=201)
def post_menu(new_menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    if crud.read_menu_by_title(new_menu.title, db):
        raise HTTPException(
            status_code=400, detail="Menu with that title already exists.")

    return crud.create_menu(new_menu, db)


@app.patch('/api/v1/menus/{menu_id}', response_model=schemas.MenuInfo)
def patch_menu(menu_id: str, patch: schemas.MenuUpdate, db: Session = Depends(get_db)):

    if not crud.read_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='menu not found')
    crud.update_menu(menu_id, patch, db)
    return crud.read_menu(menu_id, db)


@app.delete('/api/v1/menus/{menu_id}', response_model=schemas.Message)
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    if not crud.read_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='menu not found')
    crud.delete_menu(menu_id, db)
    message = {"status": True, "message": "The menu has been deleted"}
    return message


# Submenu routers
@app.get('/api/v1/menus/{menu_id}/submenus', response_model=List[schemas.SubmenuInfo])
def get_submenus(menu_id: str, db: Session = Depends(get_db)):
    return crud.read_submenus(menu_id, db)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubmenuInfo)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    submenu = crud.read_submenu(menu_id, submenu_id, db)
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@app.post('/api/v1/menus/{menu_id}/submenus', response_model=schemas.SubmenuInfo, status_code=201)
def post_submenu(menu_id: str, new_submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    if crud.read_submenu_by_title(menu_id, new_submenu.title, db):
        raise HTTPException(status_code=400, detail="Submenu with that title already exists.")
    return crud.create_submenu(menu_id, new_submenu, db)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubmenuInfo)
def patch_submenu(menu_id: str, submenu_id: str, patch: schemas.SubmenuUpdate, db: Session = Depends(get_db)):
    if not crud.read_submenu(menu_id, submenu_id, db):
        raise HTTPException(status_code=404, detail='submenu not found')
    crud.update_submenu(menu_id, submenu_id, patch, db)
    return crud.read_submenu(menu_id, submenu_id, db)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.Message)
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    if not crud.read_submenu(menu_id, submenu_id, db):
        raise HTTPException(status_code=404, detail='submenu not found')
    crud.delete_submenu(menu_id, submenu_id, db)
    message = {"status": True, "message": "The submenu has been deleted"}
    return message


# Dish routers
@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=List[schemas.DishInfo])
def get_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return crud.read_dishes(menu_id, submenu_id, db)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.DishInfo)
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    dish = crud.read_dish(menu_id, submenu_id, dish_id, db)
    if not dish:
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=schemas.DishInfo, status_code=201)
def post_dish(menu_id: str, submenu_id: str, new_dish: schemas.DishCreate, db: Session = Depends(get_db)):
    if crud.read_dish_by_title(menu_id, submenu_id, new_dish.title, db):
        raise HTTPException(status_code=400, detail="Dish with that title already exists.")
    return crud.create_dish(menu_id, submenu_id, new_dish, db)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.DishInfo)
def patch_dish(menu_id: str, submenu_id: str, dish_id: str, patch: schemas.DishUpdate, db: Session = Depends(get_db)):
    if not crud.read_dish(menu_id, submenu_id, dish_id, db):
        raise HTTPException(status_code=404, detail='dish not found')

    crud.update_dish(submenu_id, dish_id, patch, db)
    return crud.read_dish(menu_id, submenu_id, dish_id, db)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Message)
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    if not crud.read_dish(menu_id, submenu_id, dish_id, db):
        raise HTTPException(status_code=404, detail='dish not found')
    crud.delete_dish(submenu_id, dish_id, db)
    message = {"status": True, "message": "The dish has been deleted"}
    return message
