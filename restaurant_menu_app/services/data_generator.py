import json

import aiofiles  # type: ignore
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.main_db import crud
from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.schemas.scheme import (
    DishCreate,
    MenuCreate,
    Message,
    SubmenuCreate,
)


class DataGeneratorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate(self) -> Message:
        data = await DataGeneratorService.__get_data_from_source(self)
        try:
            await DataGeneratorService.__create_items(self, data)
        except Exception:
            await self.db.rollback()
            raise

        return Message(status=True, message="test data created")

    async def __get_data_from_source(self):
        source_path = "restaurant_menu_app/services/data/prepared_data.json"
        async with aiofiles.open(source_path, "r") as source:
            data = await source.read()
            data1 = json.loads(data)
        return data1

    async def __create_items(self, data, parent_id=None):
        for item in data:
            if "submenus" in item.keys():
                menu_to_create = MenuCreate(title=item["title"], description=item["description"])
                created_menu = await crud.create_menu(data=menu_to_create, db=self.db)
                child_submenus = [submenu for submenu in item["submenus"]]
                await DataGeneratorService.__create_items(self, child_submenus, parent_id=created_menu.id)

            elif "dishes" in item.keys():
                submenu_to_create = SubmenuCreate(title=item["title"], description=item["description"])
                created_submenu = await crud.create_submenu(menu_id=parent_id, data=submenu_to_create, db=self.db)
                child_dishes = [dish for dish in item["dishes"]]
                await DataGeneratorService.__create_items(self, child_dishes, parent_id=created_submenu.id)

            else:
                dish_to_create = DishCreate(title=item["title"], description=item["description"], price=item["price"])
                await crud.create_dish(submenu_id=parent_id, data=dish_to_create, db=self.db)


def get_data_generator_service(db: AsyncSession = Depends(get_db)) -> DataGeneratorService:
    return DataGeneratorService(db=db)