# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


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
        submenu_id: str,
        data: scheme.DishCreate, db: Session,
):
    new_dish = model.Dish(submenu_id=submenu_id, **data.dict())
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish.id


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
