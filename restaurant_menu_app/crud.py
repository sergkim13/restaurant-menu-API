from fastapi import HTTPException
import sqlalchemy
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas


# Menu CRUD operations
def read_menus(db: Session):
    return db.query(models.Menu).all()


def read_menu(menu_id: str, db: Session):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def read_menu_by_title(menu_title: str, db: Session):
    return db.query(models.Menu).filter(models.Menu.title == menu_title).first()


def create_menu(new_menu: schemas.MenuCreate, db: Session):
    menu = models.Menu(**new_menu.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def update_menu(menu_id: str, patch: schemas.MenuUpdate, db: Session):
    db.query(models.Menu).filter(models.Menu.id == menu_id).update(patch.dict())
    db.commit()
    return read_menu(menu_id, db)


def delete_menu(menu_id: str, db: Session):
<<<<<<< HEAD
    # db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    # message = {"status": True, "message": "The menu has been deleted"}
    # return message
=======
>>>>>>> 3dc4be9 (realaized dish crud. Didnt realize count fields)
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    db.delete(menu)
    db.commit()
    message = {"status": True, "message": "The menu has been deleted"}
    return message



# Submenu CRUD operations
def read_submenus(menu_id: str, db: Session):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()


def read_submenu(menu_id: str, submenu_id: str, db: Session):
    return db.query(models.Submenu).filter(
            models.Submenu.menu_id == menu_id,
            models.Submenu.id == submenu_id
            ).first()


def read_submenu_by_title(menu_id: str, new_submenu_title: str, db: Session):
    return db.query(models.Submenu).filter(
        models.Submenu.title == new_submenu_title,
        models.Submenu.menu_id == menu_id
    ).first()


def create_submenu(menu_id: str, new_submenu: schemas.SubmenuCreate, db: Session):
    submenu = models.Submenu(menu_id=menu_id, **new_submenu.dict())

    try:
        db.add(submenu)
        db.commit()
        db.refresh(submenu)
    except IntegrityError:
        raise HTTPException(status_code=404, detail='Menu not found')

    return submenu


def update_submenu(menu_id: str, submenu_id: str, patch: schemas.SubmenuUpdate, db: Session):
    db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id, models.Submenu.menu_id == menu_id
        ).update(patch.dict())
    db.commit()
    return read_submenu(menu_id, submenu_id, db)


def delete_submenu(menu_id: str, submenu_id: str, db: Session):
<<<<<<< HEAD
    # db.query(models.Submenu).filter(
    #     models.Submenu.id == submenu_id,
    #     models.Submenu.menu_id == menu_id
    #     ).delete()
    # message = {"status": True, "message": "The submenu has been deleted"}
    # return message
=======
>>>>>>> 3dc4be9 (realaized dish crud. Didnt realize count fields)
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id).first()
    db.delete(submenu)
    db.commit()
    message = {"status": True, "message": "The submenu has been deleted"}
    return message

# Dish CRUD operations
def read_dishes(menu_id: str, submenu_id: str, db: Session):
    return db.query(models.Dish).filter(
        models.Menu.id == models.Submenu.menu_id,
        models.Submenu.id == models.Dish.submenu_id,
        models.Menu.id == menu_id,
        models.Dish.submenu_id == submenu_id).all()


def read_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session):
    return db.query(models.Dish).join(models.Submenu).join(models.Menu).\
        filter(
            models.Menu.id == menu_id,
            models.Submenu.id == submenu_id,
            models.Dish.id == dish_id).first()


def read_dish_by_title(menu_id: str, submenu_id: str, new_dish_title: str, db: Session):
    return db.query(models.Dish).join(models.Dish.submenu).join(models.Submenu.main_menu).\
        filter(
            models.Menu.id == menu_id,
            models.Dish.submenu_id == submenu_id,
            models.Dish.title == new_dish_title).first()


def create_dish(submenu_id: str, new_dish: schemas.DishCreate, db: Session):
    dish = models.Dish(submenu_id=submenu_id, **new_dish.dict())

    try:
        db.add(dish)
        db.commit()
        db.refresh(dish)
    except IntegrityError:
        raise HTTPException(status_code=404, detail='Menu or submenu not found')

    return dish


def update_dish(menu_id: str, submenu_id: str, dish_id: str, patch: schemas.DishUpdate, db: Session):
    db.query(models.Dish).filter(
        models.Dish.id == dish_id, models.Dish.submenu_id == submenu_id
        ).update(patch.dict())
    db.commit()
    return read_dish(menu_id, submenu_id, dish_id, db)


def delete_dish(submenu_id: str, dish_id: str, db: Session):
<<<<<<< HEAD
    # db.query(models.Dish).filter(
    #     models.Dish.id == dish_id,
    #     models.Dish.submenu_id == submenu_id
    #     ).delete()
    # message = {"status": True, "message": "The dish has been deleted"}
    # return message
=======
>>>>>>> 3dc4be9 (realaized dish crud. Didnt realize count fields)
    dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id).first()
    db.delete(dish)
    db.commit()
    message = {"status": True, "message": "The dish has been deleted"}
    return message