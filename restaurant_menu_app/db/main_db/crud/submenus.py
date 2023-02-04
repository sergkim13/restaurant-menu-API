from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


async def read_submenus(menu_id: str, db: AsyncSession):
    query = (
        select(
            model.Submenu.id,
            model.Submenu.title,
            model.Submenu.description,
            func.count(model.Dish.id).label("dishes_count"),
        )
        .join(
            model.Menu,
            model.Menu.id == model.Submenu.menu_id,
        )
        .outerjoin(
            model.Dish,
            model.Dish.submenu_id == model.Submenu.id,
        )
        .where(
            model.Menu.id == menu_id,
        )
        .group_by(
            model.Submenu.id,
        )
    )
    result = await db.execute(query)
    return result.all()


async def read_submenu(menu_id: str, submenu_id: str, db: AsyncSession):
    query = (
        select(
            model.Submenu.id,
            model.Submenu.title,
            model.Submenu.description,
            func.count(model.Dish.id).label("dishes_count"),
        )
        .outerjoin(
            model.Dish,
            model.Dish.submenu_id == model.Submenu.id,
        )
        .where(
            model.Menu.id == menu_id,
            model.Submenu.id == submenu_id,
        )
        .group_by(
            model.Submenu.id,
        )
    )
    result = await db.execute(query)
    return result.first()


async def create_submenu(menu_id: str, data: scheme.SubmenuCreate, db: AsyncSession):
    new_submenu = model.Submenu(menu_id=menu_id, **data.dict())
    db.add(new_submenu)
    await db.commit()
    await db.refresh(new_submenu)
    return new_submenu


async def update_submenu(
    menu_id: str,
    submenu_id: str,
    patch: scheme.SubmenuUpdate,
    db: AsyncSession,
):
    submenu_to_update = await read_submenu(menu_id, submenu_id, db)
    values = patch.dict(exclude_unset=True)
    for key, value in values.items():
        if not value:
            values[key] = submenu_to_update[key]
    stmt = (
        update(
            model.Submenu,
        )
        .where(
            model.Submenu.id == submenu_id,
            model.Submenu.menu_id == menu_id,
        )
        .values(**values)
    )
    await db.execute(stmt)
    await db.commit()


async def delete_submenu(menu_id: str, submenu_id: str, db: AsyncSession):
    stmt = delete(
        model.Submenu,
    ).where(
        model.Submenu.id == submenu_id,
        model.Submenu.menu_id == menu_id,
    )
    await db.execute(stmt)
    await db.commit()
