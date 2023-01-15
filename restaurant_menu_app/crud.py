from sqlalchemy.orm import Session
from . import models, schemas


def get_menus(db: Session):
    return db.query(models.Menu).all()


def get_menu(menu_id: str, db: Session):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def get_menu_by_title(menu_title: str, db: Session):
    return db.query(models.Menu).filter(models.Menu.title == menu_title).first()


def add_menu(new_menu: schemas.MenuCreate, db: Session):
    menu = models.Menu(**new_menu.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def update_menu(menu_id: str, patch: schemas.MenuUpdate, db: Session):
    db.query(models.Menu).filter(models.Menu.id == menu_id).update(patch.dict())
    db.commit()
    return get_menu(menu_id, db)


def delete_menu(menu_id: str, db: Session):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    message = {"status": True, "message": "The menu has been deleted"}
    return message