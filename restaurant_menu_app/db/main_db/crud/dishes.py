from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


async def read_dishes(menu_id: str, submenu_id: str, db: AsyncSession):
    query = (
        select(
            model.Dish.id,
            model.Dish.title,
            model.Dish.description,
            model.Dish.price,
        )
        .join(
            model.Submenu,
        )
        .where(
            model.Submenu.id == submenu_id,
            model.Submenu.menu_id == menu_id,
        )
    )
    result = await db.execute(query)
    return result.all()


async def read_dish(menu_id: str, submenu_id: str, dish_id: str, db: AsyncSession):
    query = select(
        model.Dish.id,
        model.Dish.title,
        model.Dish.description,
        model.Dish.price,
    ).where(
        model.Menu.id == model.Submenu.menu_id,
        model.Submenu.id == model.Dish.submenu_id,
        model.Menu.id == menu_id,
        model.Dish.id == dish_id,
        model.Dish.submenu_id == submenu_id,
    )
    result = await db.execute(query)
    return result.first()


async def create_dish(
    submenu_id: str,
    data: scheme.DishCreate,
    db: AsyncSession,
):
    new_dish = model.Dish(submenu_id=submenu_id, **data.dict())
    db.add(new_dish)
    await db.commit()
    await db.refresh(new_dish)
    return new_dish


async def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    patch: scheme.DishUpdate,
    db: AsyncSession,
):
    dish_to_update = await read_dish(menu_id, submenu_id, dish_id, db)
    values = patch.dict(exclude_unset=True)
    for key, value in values.items():
        if not value:
            values[key] = dish_to_update[key]
    stmt = (
        update(
            model.Dish,
        )
        .where(
            model.Dish.id == dish_id,
            model.Dish.submenu_id == submenu_id,
        )
        .values(**values)
    )
    await db.execute(stmt)
    await db.commit()


async def delete_dish(submenu_id: str, dish_id: str, db: AsyncSession):
    stmt = delete(
        model.Dish,
    ).where(
        model.Dish.id == dish_id,
        model.Dish.submenu_id == submenu_id,
    )
    await db.execute(stmt)
    await db.commit()
