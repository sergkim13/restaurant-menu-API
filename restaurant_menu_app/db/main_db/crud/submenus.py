from sqlalchemy import func  # , insert, select

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


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
        menu_id: str, data: scheme.SubmenuCreate, db: Session,
):
    new_submenu = model.Submenu(menu_id=menu_id, **data.dict())
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu.id


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