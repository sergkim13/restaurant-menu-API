import json
from http import HTTPStatus
from pathlib import Path

import aiofiles  # type: ignore
from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.main_db.crud.abstract_crud import AbstractCRUD
from restaurant_menu_app.db.main_db.crud.dishes import DishCRUD
from restaurant_menu_app.db.main_db.crud.helpers import HelperCRUD
from restaurant_menu_app.db.main_db.crud.menus import MenuCRUD
from restaurant_menu_app.db.main_db.crud.submenus import SubmenuCRUD
from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.schemas.scheme import (
    DishCreate,
    MenuCreate,
    Message,
    SubmenuCreate,
)
from restaurant_menu_app.tasks import tasks


class HelperServise:
    def __init__(
        self,
        db: AsyncSession,
        helper_crud: HelperCRUD,
        menu_crud: AbstractCRUD,
        submenu_crud: AbstractCRUD,
        dish_crud: AbstractCRUD,
    ) -> None:
        self.db = db
        self.helper_crud = helper_crud
        self.menu_crud = menu_crud
        self.submenu_crud = submenu_crud
        self.dish_crud = dish_crud

    async def put_all_data_to_file(self) -> Message:
        data = await self.helper_crud.get_all()
        if data is None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Database is empty!",
            )

        task = tasks.save_data_to_file.delay(data)
        return Message(status=True, message=f"Task registred with ID: {task.id}")

    def get_all_data_in_file(self, task_id: str):
        task = tasks.get_result(task_id)
        if task.ready():
            filename = task.result["file_name"]
            filepath = str(Path("src").parent.absolute().joinpath("data", filename))
            return FileResponse(
                path=filepath,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename={filename}"},
            )
        else:
            return {"task_id": task_id, "status": task.status}

    async def generate_test_data(self) -> Message:
        data = await self.get_data_from_source()
        try:
            await self.create_items(data)
        except Exception:
            await self.db.rollback()
            raise

        return Message(status=True, message="test data created")

    async def get_data_from_source(self):
        source_path = "restaurant_menu_app/services/data/prepared_data.json"
        async with aiofiles.open(source_path, "r") as source:
            data = await source.read()
            data1 = json.loads(data)
        return data1

    async def create_items(self, data, parent_id=None):
        for item in data:
            if "submenus" in item.keys():
                menu_to_create = MenuCreate(title=item["title"], description=item["description"])
                created_menu = await self.menu_crud.create(data=menu_to_create)
                child_submenus = [submenu for submenu in item["submenus"]]
                await self.create_items(child_submenus, parent_id=created_menu.id)

            elif "dishes" in item.keys():
                submenu_to_create = SubmenuCreate(title=item["title"], description=item["description"])
                created_submenu = await self.submenu_crud.create(menu_id=parent_id, data=submenu_to_create)
                child_dishes = [dish for dish in item["dishes"]]
                await self.create_items(child_dishes, parent_id=created_submenu.id)

            else:
                dish_to_create = DishCreate(title=item["title"], description=item["description"], price=item["price"])
                await self.dish_crud.create(submenu_id=parent_id, data=dish_to_create)


def get_helper_service(db: AsyncSession = Depends(get_db)) -> HelperServise:
    helper_crud = HelperCRUD(db=db)
    menu_crud = MenuCRUD(db=db)
    submenu_crud = SubmenuCRUD(db=db)
    dish_crud = DishCRUD(db=db)
    return HelperServise(
        db=db,
        helper_crud=helper_crud,
        menu_crud=menu_crud,
        submenu_crud=submenu_crud,
        dish_crud=dish_crud,
    )
