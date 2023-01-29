from fastapi import HTTPException
from sqlalchemy import distinct, func  # , insert, select
from sqlalchemy.exc import IntegrityError

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ...models import model
from ...schemas import scheme


def read_menus(db: Session):
    return db.query(
        model.Menu.id,
        model.Menu.title,
        model.Menu.description,
        func.count(distinct(model.Submenu.id)).label('submenus_count'),
        func.count(model.Dish.id).label('dishes_count'),
    ).join(
        model.Submenu,
        model.Submenu.menu_id == model.Menu.id,
        isouter=True,
    ).join(
        model.Dish,
        model.Dish.submenu_id == model.Submenu.id,
        isouter=True,
    ).group_by(model.Menu.id).all()


def read_menu(menu_id: str, db: Session):
    return db.query(
        model.Menu.id,
        model.Menu.title,
        model.Menu.description,
        func.count(distinct(model.Submenu.id)).label('submenus_count'),
        func.count(model.Dish.id).label('dishes_count'),
    ).join(
        model.Submenu,
        model.Submenu.menu_id == model.Menu.id,
        isouter=True,
    ).join(
        model.Dish,
        model.Dish.submenu_id == model.Submenu.id,
        isouter=True,
    ).filter(
        model.Menu.id == menu_id,
    ).group_by(model.Menu.id).first()


def read_menu_by_title(menu_title: str, db: Session):
    return db.query(model.Menu).filter(
        model.Menu.title == menu_title,
    ).first()


def create_menu(new_menu: scheme.MenuCreate, db: Session):
    menu = model.Menu(**new_menu.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return read_menu(menu.id, db)


def update_menu(menu_id: str, patch: scheme.MenuUpdate, db: Session):
    db.query(model.Menu).filter(
        model.Menu.id == menu_id,
    ).update(patch.dict())
    db.commit()


def delete_menu(menu_id: str, db: Session):
    menu = db.query(model.Menu).filter(model.Menu.id == menu_id).first()
    db.delete(menu)
    db.commit()


# Submenu CRUD operations
def read_submenus(menu_id: str, db: Session):
    return db.query(
        model.Submenu.id,
        model.Submenu.title,
        model.Submenu.description,
        func.count(model.Dish.id).label('dishes_count'),
    ).join(
        model.Menu,
        model.Menu.id == model.Submenu.menu_id,
    ).join(
        model.Dish,
        model.Dish.submenu_id == model.Submenu.id,
        isouter=True,
    ).filter(
        model.Menu.id == menu_id,
    ).group_by(model.Submenu.id).all()


def read_submenu(menu_id: str, submenu_id: str, db: Session):
    return db.query(
        model.Submenu.id,
        model.Submenu.title,
        model.Submenu.description,
        func.count(model.Dish.id).label('dishes_count'),
    ).join(
        model.Menu,
        model.Menu.id == model.Submenu.menu_id,
    ).join(
        model.Dish,
        model.Dish.submenu_id == model.Submenu.id,
        isouter=True,
    ).filter(
        model.Menu.id == menu_id,
        model.Submenu.id == submenu_id,
    ).group_by(model.Submenu.id).first()


def read_submenu_by_title(menu_id: str, new_submenu_title: str, db: Session):
    return db.query(model.Submenu).filter(
        model.Submenu.title == new_submenu_title,
        model.Submenu.menu_id == menu_id,
    ).first()


def create_submenu(
        menu_id: str, new_submenu: scheme.SubmenuCreate, db: Session,
):

    submenu = model.Submenu(menu_id=menu_id, **new_submenu.dict())

    try:
        db.add(submenu)
        db.commit()
        db.refresh(submenu)
    except IntegrityError:
        raise HTTPException(status_code=404, detail='Menu not found')

    return read_submenu(menu_id, submenu.id, db)


def update_submenu(
        menu_id: str, submenu_id: str,
        patch: scheme.SubmenuUpdate, db: Session,
):

    db.query(model.Submenu).filter(
        model.Submenu.id == submenu_id, model.Submenu.menu_id == menu_id,
    ).update(patch.dict())
    db.commit()


def delete_submenu(menu_id: str, submenu_id: str, db: Session):
    submenu = db.query(model.Submenu).filter(
        model.Submenu.id == submenu_id,
        model.Submenu.menu_id == menu_id,
    ).first()
    db.delete(submenu)
    db.commit()


# Dish CRUD operations
def read_dishes(menu_id: str, submenu_id: str, db: Session):
    return db.query(model.Dish).filter(
        model.Menu.id == model.Submenu.menu_id,
        model.Submenu.id == model.Dish.submenu_id,
        model.Menu.id == menu_id,
        model.Dish.submenu_id == submenu_id,
    ).all()


def read_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session):
    return db.query(model.Dish).join(
        model.Submenu,
    ).join(
        model.Menu,
    ).filter(
        model.Menu.id == menu_id,
        model.Submenu.id == submenu_id,
        model.Dish.id == dish_id,
    ).first()


def read_dish_by_title(
        menu_id: str, submenu_id: str, new_dish_title: str, db: Session,
):

    return db.query(model.Dish).join(
        model.Dish.submenu,
    ).join(
        model.Submenu.main_menu,
    ).filter(
        model.Menu.id == menu_id,
        model.Dish.submenu_id == submenu_id,
        model.Dish.title == new_dish_title,
    ).first()


def create_dish(
        menu_id: str, submenu_id: str,
        new_dish: scheme.DishCreate, db: Session,
):

    dish = model.Dish(submenu_id=submenu_id, **new_dish.dict())

    try:
        db.add(dish)
        db.commit()
        db.refresh(dish)
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail='Menu or submenu not found',
        )

    return read_dish(menu_id, submenu_id, dish.id, db)


def update_dish(
        submenu_id: str, dish_id: str,
        patch: scheme.DishUpdate, db: Session,
):

    db.query(model.Dish).filter(
        model.Dish.id == dish_id,
        model.Dish.submenu_id == submenu_id,
    ).update(patch.dict())
    db.commit()


def delete_dish(submenu_id: str, dish_id: str, db: Session):
    dish = db.query(model.Dish).filter(
        model.Dish.id == dish_id,
        model.Dish.submenu_id == submenu_id,
    ).first()
    db.delete(dish)
    db.commit()
