from fastapi import HTTPException
from sqlalchemy import distinct, func  # , insert, select
from sqlalchemy.exc import IntegrityError

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import models, schemas


def read_menus(db: Session):
    return db.query(
        models.Menu.id,
        models.Menu.title,
        models.Menu.description,
        func.count(distinct(models.Submenu.id)).label('submenus_count'),
        func.count(models.Dish.id).label('dishes_count'),
    ).join(
        models.Submenu,
        models.Submenu.menu_id == models.Menu.id,
        isouter=True,
    ).join(
        models.Dish,
        models.Dish.submenu_id == models.Submenu.id,
        isouter=True,
    ).group_by(models.Menu.id).all()


def read_menu(menu_id: str, db: Session):
    return db.query(
        models.Menu.id,
        models.Menu.title,
        models.Menu.description,
        func.count(distinct(models.Submenu.id)).label('submenus_count'),
        func.count(models.Dish.id).label('dishes_count'),
    ).join(
        models.Submenu,
        models.Submenu.menu_id == models.Menu.id,
        isouter=True,
    ).join(
        models.Dish,
        models.Dish.submenu_id == models.Submenu.id,
        isouter=True,
    ).filter(
        models.Menu.id == menu_id,
    ).group_by(models.Menu.id).first()


def read_menu_by_title(menu_title: str, db: Session):
    return db.query(models.Menu).filter(
        models.Menu.title == menu_title,
    ).first()


def create_menu(new_menu: schemas.MenuCreate, db: Session):
    menu = models.Menu(**new_menu.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return read_menu(menu.id, db)


def update_menu(menu_id: str, patch: schemas.MenuUpdate, db: Session):
    db.query(models.Menu).filter(
        models.Menu.id == menu_id,
    ).update(patch.dict())
    db.commit()


def delete_menu(menu_id: str, db: Session):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    db.delete(menu)
    db.commit()


# Submenu CRUD operations
def read_submenus(menu_id: str, db: Session):
    return db.query(
        models.Submenu.id,
        models.Submenu.title,
        models.Submenu.description,
        func.count(models.Dish.id).label('dishes_count'),
    ).join(
        models.Menu,
        models.Menu.id == models.Submenu.menu_id,
    ).join(
        models.Dish,
        models.Dish.submenu_id == models.Submenu.id,
        isouter=True,
    ).filter(
        models.Menu.id == menu_id,
    ).group_by(models.Submenu.id).all()


def read_submenu(menu_id: str, submenu_id: str, db: Session):
    return db.query(
        models.Submenu.id,
        models.Submenu.title,
        models.Submenu.description,
        func.count(models.Dish.id).label('dishes_count'),
    ).join(
        models.Menu,
        models.Menu.id == models.Submenu.menu_id,
    ).join(
        models.Dish,
        models.Dish.submenu_id == models.Submenu.id,
        isouter=True,
    ).filter(
        models.Menu.id == menu_id,
        models.Submenu.id == submenu_id,
    ).group_by(models.Submenu.id).first()


def read_submenu_by_title(menu_id: str, new_submenu_title: str, db: Session):
    return db.query(models.Submenu).filter(
        models.Submenu.title == new_submenu_title,
        models.Submenu.menu_id == menu_id,
    ).first()


def create_submenu(
        menu_id: str, new_submenu: schemas.SubmenuCreate, db: Session,
):

    submenu = models.Submenu(menu_id=menu_id, **new_submenu.dict())

    try:
        db.add(submenu)
        db.commit()
        db.refresh(submenu)
    except IntegrityError:
        raise HTTPException(status_code=404, detail='Menu not found')

    return read_submenu(menu_id, submenu.id, db)


def update_submenu(
        menu_id: str, submenu_id: str,
        patch: schemas.SubmenuUpdate, db: Session,
):

    db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id, models.Submenu.menu_id == menu_id,
    ).update(patch.dict())
    db.commit()


def delete_submenu(menu_id: str, submenu_id: str, db: Session):
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id,
    ).first()
    db.delete(submenu)
    db.commit()


# Dish CRUD operations
def read_dishes(menu_id: str, submenu_id: str, db: Session):
    return db.query(models.Dish).filter(
        models.Menu.id == models.Submenu.menu_id,
        models.Submenu.id == models.Dish.submenu_id,
        models.Menu.id == menu_id,
        models.Dish.submenu_id == submenu_id,
    ).all()


def read_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session):
    return db.query(models.Dish).join(
        models.Submenu,
    ).join(
        models.Menu,
    ).filter(
        models.Menu.id == menu_id,
        models.Submenu.id == submenu_id,
        models.Dish.id == dish_id,
    ).first()


def read_dish_by_title(
        menu_id: str, submenu_id: str, new_dish_title: str, db: Session,
):

    return db.query(models.Dish).join(
        models.Dish.submenu,
    ).join(
        models.Submenu.main_menu,
    ).filter(
        models.Menu.id == menu_id,
        models.Dish.submenu_id == submenu_id,
        models.Dish.title == new_dish_title,
    ).first()


def create_dish(
        menu_id: str, submenu_id: str,
        new_dish: schemas.DishCreate, db: Session,
):

    dish = models.Dish(submenu_id=submenu_id, **new_dish.dict())

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
        patch: schemas.DishUpdate, db: Session,
):

    db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id,
    ).update(patch.dict())
    db.commit()


def delete_dish(submenu_id: str, dish_id: str, db: Session):
    dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id,
    ).first()
    db.delete(dish)
    db.commit()


# # Menu CRUD operations
# async def read_menus(db: AsyncSession):
#     query = select(
#         models.Menu.id,
#         models.Menu.title,
#         models.Menu.description,
#         func.count(distinct(models.Submenu.id)).label('submenus_count'),
#         func.count(models.Dish.id).label('dishes_count')
#     ).join(
#         models.Submenu,
#         models.Submenu.menu_id == models.Menu.id,
#         isouter=True,
#     ).join(
#         models.Dish,
#         models.Dish.submenu_id == models.Submenu.id,
#         isouter=True,
#     ).group_by(models.Menu.id)
#     result = await db.execute(query)
#     return result.all()
#     # return db.(
#     #     models.Menu.id,
#     #     models.Menu.title,
#     #     models.Menu.description,
#     #     func.count(distinct(models.Submenu.id)).label('submenus_count'),
#     #     func.count(models.Dish.id).label('dishes_count'),
#     # ).join(
#     #     models.Submenu,
#     #     models.Submenu.menu_id == models.Menu.id,
#     #     isouter=True,
#     # ).join(
#     #     models.Dish,
#     #     models.Dish.submenu_id == models.Submenu.id,
#     #     isouter=True,
#     # ).group_by(models.Menu.id).all()


# async def read_menu(menu_id: int, db: AsyncSession):
#     query = select(
#         models.Menu.id,
#         models.Menu.title,
#         models.Menu.description,
#         func.count(distinct(models.Submenu.id)).label('submenus_count'),
#         func.count(models.Dish.id).label('dishes_count'),
#     ).join(
#         models.Submenu,
#         models.Submenu.menu_id == models.Menu.id,
#         isouter=True,
#     ).join(
#         models.Dish,
#         models.Dish.submenu_id == models.Submenu.id,
#         isouter=True,
#     ).filter(
#         models.Menu.id == menu_id,
#     ).group_by(models.Menu.id)
#     result = await db.execute(query)
#     return result.first()

#     # return db.query(
#     #     models.Menu.id,
#     #     models.Menu.title,
#     #     models.Menu.description,
#     #     func.count(distinct(models.Submenu.id)).label('submenus_count'),
#     #     func.count(models.Dish.id).label('dishes_count'),
#     # ).join(
#     #     models.Submenu,
#     #     models.Submenu.menu_id == models.Menu.id,
#     #     isouter=True,
#     # ).join(
#     #     models.Dish,
#     #     models.Dish.submenu_id == models.Submenu.id,
#     #     isouter=True,
#     # ).filter(
#     #     models.Menu.id == menu_id,
#     # ).group_by(models.Menu.id).first()


# async def read_menu_by_title(menu_title: str, db: AsyncSession):
#     query = select(models.Menu).where(
#         models.Menu.title == menu_title)
#     print('Искомое название:', menu_title)
#     print(query)
#     result = await db.execute(query)
#     return result.first()

#     # return db.query(models.Menu).filter(
#     #     models.Menu.title == menu_title,
#     # ).first()


# async def create_menu(new_menu: schemas.MenuCreate, db: AsyncSession):
#     # statement = models.Menu.insert().values(**new_menu.dict())
#     menu = models.Menu(**new_menu.dict())
#     # db.execute(statement)
#     await db.add(menu)
#     await db.commit()
#     await db.refresh(statement)
#     return await read_menu(menu.id, db)


# async def update_menu(menu_id: str, patch: schemas.MenuUpdate, db: AsyncSession):
#     db.query(models.Menu).filter(
#         models.Menu.id == menu_id,
#     ).update(patch.dict())
#     db.commit()


# async def delete_menu(menu_id: str, db: AsyncSession):
#     menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
#     db.delete(menu)
#     db.commit()


# # Submenu CRUD operations
# async def read_submenus(menu_id: str, db: AsyncSession):
#     return db.query(
#         models.Submenu.id,
#         models.Submenu.title,
#         models.Submenu.description,
#         func.count(models.Dish.id).label('dishes_count'),
#     ).join(
#         models.Menu,
#         models.Menu.id == models.Submenu.menu_id,
#     ).join(
#         models.Dish,
#         models.Dish.submenu_id == models.Submenu.id,
#         isouter=True,
#     ).filter(
#         models.Menu.id == menu_id,
#     ).group_by(models.Submenu.id).all()


# async def read_submenu(menu_id: str, submenu_id: str, db: AsyncSession):
#     return db.query(
#         models.Submenu.id,
#         models.Submenu.title,
#         models.Submenu.description,
#         func.count(models.Dish.id).label('dishes_count'),
#     ).join(
#         models.Menu,
#         models.Menu.id == models.Submenu.menu_id,
#     ).join(
#         models.Dish,
#         models.Dish.submenu_id == models.Submenu.id,
#         isouter=True,
#     ).filter(
#         models.Menu.id == menu_id,
#         models.Submenu.id == submenu_id,
#     ).group_by(models.Submenu.id).first()


# async def read_submenu_by_title(menu_id: str, new_submenu_title: str, db: AsyncSession):
#     return db.query(models.Submenu).filter(
#         models.Submenu.title == new_submenu_title,
#         models.Submenu.menu_id == menu_id,
#     ).first()


# async def create_submenu(
#         menu_id: str, new_submenu: schemas.SubmenuCreate, db: AsyncSession,
# ):

#     submenu = models.Submenu(menu_id=menu_id, **new_submenu.dict())

#     try:
#         db.add(submenu)
#         db.commit()
#         db.refresh(submenu)
#     except IntegrityError:
#         raise HTTPException(status_code=404, detail='Menu not found')

#     return read_submenu(menu_id, submenu.id, db)


# async def update_submenu(
#         menu_id: str, submenu_id: str,
#         patch: schemas.SubmenuUpdate, db: AsyncSession,
# ):

#     db.query(models.Submenu).filter(
#         models.Submenu.id == submenu_id, models.Submenu.menu_id == menu_id,
#     ).update(patch.dict())
#     db.commit()


# async def delete_submenu(menu_id: str, submenu_id: str, db: AsyncSession):
#     submenu = db.query(models.Submenu).filter(
#         models.Submenu.id == submenu_id,
#         models.Submenu.menu_id == menu_id,
#     ).first()
#     db.delete(submenu)
#     db.commit()


# # Dish CRUD operations
# async def read_dishes(menu_id: str, submenu_id: str, db: AsyncSession):
#     return db.query(models.Dish).filter(
#         models.Menu.id == models.Submenu.menu_id,
#         models.Submenu.id == models.Dish.submenu_id,
#         models.Menu.id == menu_id,
#         models.Dish.submenu_id == submenu_id,
#     ).all()


# async def read_dish(menu_id: str, submenu_id: str, dish_id: str, db: AsyncSession):
#     return db.query(models.Dish).join(
#         models.Submenu,
#     ).join(
#         models.Menu,
#     ).filter(
#         models.Menu.id == menu_id,
#         models.Submenu.id == submenu_id,
#         models.Dish.id == dish_id,
#     ).first()


# async def read_dish_by_title(
#         menu_id: str, submenu_id: str, new_dish_title: str, db: AsyncSession,
# ):

#     return db.query(models.Dish).join(
#         models.Dish.submenu,
#     ).join(
#         models.Submenu.main_menu,
#     ).filter(
#         models.Menu.id == menu_id,
#         models.Dish.submenu_id == submenu_id,
#         models.Dish.title == new_dish_title,
#     ).first()


# async def create_dish(
#         menu_id: str, submenu_id: str,
#         new_dish: schemas.DishCreate, db: AsyncSession,
# ):

#     dish = models.Dish(submenu_id=submenu_id, **new_dish.dict())

#     try:
#         db.add(dish)
#         db.commit()
#         db.refresh(dish)
#     except IntegrityError:
#         raise HTTPException(
#             status_code=404, detail='Menu or submenu not found',
#         )

#     return read_dish(menu_id, submenu_id, dish.id, db)


# async def update_dish(
#         submenu_id: str, dish_id: str,
#         patch: schemas.DishUpdate, db: AsyncSession,
# ):

#     db.query(models.Dish).filter(
#         models.Dish.id == dish_id,
#         models.Dish.submenu_id == submenu_id,
#     ).update(patch.dict())
#     db.commit()


# async def delete_dish(submenu_id: str, dish_id: str, db: AsyncSession):
#     dish = db.query(models.Dish).filter(
#         models.Dish.id == dish_id,
#         models.Dish.submenu_id == submenu_id,
#     ).first()
#     db.delete(dish)
#     db.commit()
