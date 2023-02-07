from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.cache.cache_utils import (
    clear_cache,
    get_cache,
    is_cached,
    set_cache,
)
from restaurant_menu_app.db.main_db.crud.submenus import SubmenuCRUD
from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.schemas.scheme import (
    Message,
    SubmenuCreate,
    SubmenuInfo,
    SubmenuUpdate,
)


class SubmenuService:
    def __init__(self, submenu_crud: SubmenuCRUD) -> None:
        self.submenu_crud = submenu_crud

    async def get_list(self, menu_id: str) -> list[SubmenuInfo]:
        """Получить список подменю."""

        if await is_cached("submenu", "all"):
            return await get_cache("submenu", "all")

        submenus = await self.submenu_crud.read_all(menu_id)
        await set_cache("submenu", "all", submenus)
        return submenus

    async def get_info(self, menu_id: str, submenu_id: str) -> SubmenuInfo:
        """Получить информацию о подменю."""

        if await is_cached("submenu", submenu_id):
            return await get_cache("submenu", submenu_id)

        submenu = await self.submenu_crud.read(menu_id, submenu_id)
        if not submenu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="submenu not found",
            )
        await set_cache("submenu", submenu_id, submenu)
        return submenu

    async def create(self, menu_id: str, data: SubmenuCreate) -> SubmenuInfo:
        """Создать подменю."""

        try:
            new_submenu = await self.submenu_crud.create(menu_id, data)
        except IntegrityError as e:
            if "UniqueViolationError" in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Submenu with that title already exists",
                )
            elif "ForeignKeyViolationError" in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="parent menu not found",
                )
            else:
                raise

        created_submenu = await self.submenu_crud.read(menu_id, new_submenu.id)
        await set_cache("submenu", new_submenu.id, created_submenu)
        # Чистим кэш для родительских элементов и получения списков элементов
        await clear_cache("submenu", "all")
        await clear_cache("menu", menu_id)
        await clear_cache("menu", "all")
        return created_submenu

    async def update(self, menu_id: str, submenu_id: str, patch: SubmenuUpdate) -> SubmenuInfo:
        """Обновить подменю."""

        if not await self.submenu_crud.read(menu_id, submenu_id):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="submenu not found",
            )

        await self.submenu_crud.update(menu_id, submenu_id, patch)
        updated_submenu = await self.submenu_crud.read(menu_id, submenu_id)
        await set_cache("submenu", submenu_id, updated_submenu)
        # чистим кэш получения списка подменю
        await clear_cache("submenu", "all")
        return updated_submenu

    async def delete(self, menu_id: str, submenu_id: str) -> Message:
        """Удалить подменю."""

        if not await self.submenu_crud.read(menu_id, submenu_id):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="submenu not found",
            )

        await self.submenu_crud.delete(menu_id, submenu_id)
        await clear_cache("submenu", submenu_id)
        # Чистим кэш для родительских элементов и получения списков элементов
        await clear_cache("submenu", "all")
        await clear_cache("menu", menu_id)
        await clear_cache("menu", "all")
        return Message(status=True, message="The submenu has been deleted")


def get_submenu_service(db: AsyncSession = Depends(get_db)) -> SubmenuService:
    submenu_crud = SubmenuCRUD(db=db)
    return SubmenuService(submenu_crud=submenu_crud)
