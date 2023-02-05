from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.tasks.tasks import create_task


class TaskServise:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_task_for_get_all_content_in_xlsx(self):
        task_id = create_task(self.db)
        return task_id


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskServise:
    return TaskServise(db=db)
