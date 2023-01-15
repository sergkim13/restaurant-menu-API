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


@app.get('/api/v1/menus', response_model=List[schemas.MenuInfo])
def read_menus(db: Session = Depends(get_db)):
    menus = crud.get_menus(db)
    return menus


@app.get('/api/v1/menus/{menu_id}', response_model=schemas.MenuInfo)
def read_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = crud.get_menu(menu_id, db)
    if not menu:
        raise HTTPException(status_code=404, detail='Menu not found.')
    return menu


@app.post('/api/v1/menus', response_model=schemas.MenuInfo)
def create_menu(new_menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    if crud.get_menu_by_title(new_menu.title, db):
        raise HTTPException(status_code=400, detail="Menu with that title already exists.")
    return crud.add_menu(new_menu, db)


@app.patch('/api/v1/menus/{menu_id}', response_model=schemas.MenuInfo)
def patch_menu(menu_id: str, patch: schemas.MenuUpdate, db: Session = Depends(get_db)):
    if not crud.get_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='Menu not found.')
    updated_menu = crud.update_menu(menu_id, patch, db)
    return updated_menu


@app.delete('/app/v1/menus/{menu_id}', response_model=schemas.Message)
def erase_menu(menu_id: str, db: Session = Depends(get_db)):
    if not crud.get_menu(menu_id, db):
        raise HTTPException(status_code=404, detail='Menu not found.')
    result = crud.delete_menu(menu_id, db)
    return result


@app.get('/api/v1/menus/{menu_id}/submenus')
def get_submenus(menu_id):
    pass


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def get_submenu(menu_id, submenu_id):
    pass


@app.post('/api/v1/menus/{menu_id}/submenus')
def post_submenu(menu_id):
    pass


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def patch_submenu(menu_id, submenu_id):
    pass


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id, submenu_id):
    pass


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def get_dishes(menu_id, submenu_id):
    pass


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def get_dish(menu_id, submenu_id, dish_id):
    pass


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def post_dish(menu_id, submenu_id):
    pass


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id, submenu_id, dish_id):
    pass
