import json
from http import HTTPStatus
from pathlib import Path

import aiofiles  # type: ignore
from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.main_db import crud
from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.schemas.scheme import (
    DishCreate,
    MenuCreate,
    Message,
    SubmenuCreate,
)
from restaurant_menu_app.services.service_mixin import ServiceMixin
from restaurant_menu_app.tasks import tasks


class HelperServise(ServiceMixin):
    async def put_all_data_to_file(self) -> Message:
        data = await crud.get_all(self.db)
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
        data = await HelperServise.__get_data_from_source(self)
        try:
            await HelperServise.__create_items(self, data)
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
                await HelperServise.__create_items(self, child_submenus, parent_id=created_menu.id)

            elif "dishes" in item.keys():
                submenu_to_create = SubmenuCreate(title=item["title"], description=item["description"])
                created_submenu = await crud.create_submenu(menu_id=parent_id, data=submenu_to_create, db=self.db)
                child_dishes = [dish for dish in item["dishes"]]
                await HelperServise.__create_items(self, child_dishes, parent_id=created_submenu.id)

            else:
                dish_to_create = DishCreate(title=item["title"], description=item["description"], price=item["price"])
                await crud.create_dish(submenu_id=parent_id, data=dish_to_create, db=self.db)


def get_helper_service(db: AsyncSession = Depends(get_db)) -> HelperServise:
    return HelperServise(db=db)
