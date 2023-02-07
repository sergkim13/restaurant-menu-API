from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.main_db.crud.abstract_crud import AbstractCRUD
from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


class SubmenuCRUD(AbstractCRUD):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def read_all(self, menu_id: str):
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
        result = await self.db.execute(query)
        return result.all()

    async def read(self, menu_id: str, submenu_id: str):
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
                model.Submenu.menu_id == menu_id,
                model.Submenu.id == submenu_id,
            )
            .group_by(
                model.Submenu.id,
            )
        )
        result = await self.db.execute(query)
        return result.first()

    async def create(self, menu_id: str, data: scheme.SubmenuCreate):
        new_submenu = model.Submenu(menu_id=menu_id, **data.dict())
        self.db.add(new_submenu)
        await self.db.commit()
        await self.db.refresh(new_submenu)
        return new_submenu

    async def update(
        self,
        menu_id: str,
        submenu_id: str,
        patch: scheme.SubmenuUpdate,
    ):
        submenu_to_update = await self.read(menu_id, submenu_id)
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
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete(self, menu_id: str, submenu_id: str):
        stmt = delete(
            model.Submenu,
        ).where(
            model.Submenu.id == submenu_id,
            model.Submenu.menu_id == menu_id,
        )
        await self.db.execute(stmt)
        await self.db.commit()


def get_submenu_crud(db: AsyncSession) -> SubmenuCRUD:
    return SubmenuCRUD(db=db)
