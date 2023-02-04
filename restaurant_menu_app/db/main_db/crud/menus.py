from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


async def read_menus(db: AsyncSession):
    query = (
        select(
            model.Menu.id,
            model.Menu.title,
            model.Menu.description,
            func.count(distinct(model.Submenu.id)).label("submenus_count"),
            func.count(model.Dish.id).label("dishes_count"),
        )
        .outerjoin(
            model.Submenu,
            model.Submenu.menu_id == model.Menu.id,
        )
        .outerjoin(
            model.Dish,
            model.Dish.submenu_id == model.Submenu.id,
        )
        .group_by(
            model.Menu.id,
        )
    )
    result = await db.execute(query)
    return result.all()


async def read_menu(menu_id: str, db: AsyncSession):
    query = (
        select(
            model.Menu.id,
            model.Menu.title,
            model.Menu.description,
            func.count(distinct(model.Submenu.id)).label("submenus_count"),
            func.count(model.Dish.id).label("dishes_count"),
        )
        .outerjoin(
            model.Submenu,
            model.Submenu.menu_id == model.Menu.id,
        )
        .outerjoin(
            model.Dish,
            model.Dish.submenu_id == model.Submenu.id,
        )
        .where(
            model.Menu.id == menu_id,
        )
        .group_by(
            model.Menu.id,
        )
    )
    result = await db.execute(query)
    return result.first()


async def create_menu(data: scheme.MenuCreate, db: AsyncSession):
    new_menu = model.Menu(**data.dict())
    db.add(new_menu)
    await db.commit()
    await db.refresh(new_menu)
    return new_menu


async def update_menu(menu_id: str, patch: scheme.MenuUpdate, db: AsyncSession):
    menu_to_update = await read_menu(menu_id, db)
    values = patch.dict(exclude_unset=True)
    for key, value in values.items():
        if not value:
            values[key] = menu_to_update[key]
    stmt = (
        update(
            model.Menu,
        )
        .where(
            model.Menu.id == menu_id,
        )
        .values(**values)
    )
    await db.execute(stmt)
    await db.commit()


async def delete_menu(menu_id: str, db: AsyncSession):
    stmt = delete(model.Menu).where(model.Menu.id == menu_id)
    await db.execute(stmt)
    await db.commit()
