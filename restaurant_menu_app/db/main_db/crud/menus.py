from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.main_db.crud.abstract_crud import AbstractCRUD
from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


class MenuCRUD(AbstractCRUD):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def read_all(self):
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
        result = await self.db.execute(query)
        return result.all()

    async def read(self, menu_id: str):
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
        result = await self.db.execute(query)
        return result.first()

    async def create(self, data: scheme.MenuCreate):
        new_menu = model.Menu(**data.dict())
        self.db.add(new_menu)
        await self.db.commit()
        await self.db.refresh(new_menu)
        return new_menu

    async def update(self, menu_id: str, patch: scheme.MenuUpdate):
        menu_to_update = await self.read(menu_id)
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
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete(self, menu_id: str):
        stmt = delete(model.Menu).where(model.Menu.id == menu_id)
        await self.db.execute(stmt)
        await self.db.commit()


def get_menu_crud(db: AsyncSession) -> MenuCRUD:
    return MenuCRUD(db=db)
