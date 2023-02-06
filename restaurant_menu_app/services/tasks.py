from pathlib import Path

from fastapi import Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.main_db import crud
from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.schemas.scheme import Message
from restaurant_menu_app.tasks import tasks


class TaskServise:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def task_to_download_all_data(self) -> Message:
        data = await crud.get_all(self.db)
        task = tasks.save_data_to_file.delay(data)
        return Message(status=True, message=f"Task registred with ID: {task.id}")

    def get_task_result(self, task_id: str):
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


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskServise:
    return TaskServise(db=db)
