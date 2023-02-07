from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.main_db.crud.abstract_crud import AbstractCRUD
from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


class DishCRUD(AbstractCRUD):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def read_all(self, menu_id: str, submenu_id: str):
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
        result = await self.db.execute(query)
        return result.all()

    async def read(self, menu_id: str, submenu_id: str, dish_id: str):
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
        result = await self.db.execute(query)
        return result.first()

    async def create(self, submenu_id: str, data: scheme.DishCreate):
        new_dish = model.Dish(submenu_id=submenu_id, **data.dict())
        self.db.add(new_dish)
        await self.db.commit()
        await self.db.refresh(new_dish)
        return new_dish

    async def update(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        patch: scheme.DishUpdate,
    ):
        dish_to_update = await self.read(menu_id, submenu_id, dish_id)
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
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete(self, submenu_id: str, dish_id: str):
        stmt = delete(
            model.Dish,
        ).where(
            model.Dish.id == dish_id,
            model.Dish.submenu_id == submenu_id,
        )
        await self.db.execute(stmt)
        await self.db.commit()


def get_dish_crud(db: AsyncSession) -> DishCRUD:
    return DishCRUD(db=db)
