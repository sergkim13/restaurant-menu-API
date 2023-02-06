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
from restaurant_menu_app.db.main_db import crud
from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.schemas.scheme import (
    Message,
    SubmenuCreate,
    SubmenuInfo,
    SubmenuUpdate,
)
from restaurant_menu_app.services.service_mixin import ServiceMixin


class SubmenuService(ServiceMixin):
    async def get_list(self, menu_id: str) -> list[SubmenuInfo]:
        """Получить список подменю."""

        if await is_cached("submenu", "all"):
            return await get_cache("submenu", "all")

        submenus = await crud.read_submenus(menu_id, self.db)
        await set_cache("submenu", "all", submenus)
        return submenus

    async def get_info(self, menu_id: str, submenu_id: str) -> SubmenuInfo:
        """Получить информацию о подменю."""

        if await is_cached("submenu", submenu_id):
            return await get_cache("submenu", submenu_id)

        submenu = await crud.read_submenu(menu_id, submenu_id, self.db)
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
            new_submenu = await crud.create_submenu(menu_id, data, self.db)
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

        created_submenu = await crud.read_submenu(menu_id, new_submenu.id, self.db)
        await set_cache("submenu", new_submenu.id, created_submenu)
        # Чистим кэш для родительских элементов и получения списков элементов
        await clear_cache("submenu", "all")
        await clear_cache("menu", menu_id)
        await clear_cache("menu", "all")
        return created_submenu

    async def update(self, menu_id: str, submenu_id: str, patch: SubmenuUpdate) -> SubmenuInfo:
        """Обновить подменю."""

        if not await crud.read_submenu(menu_id, submenu_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="submenu not found",
            )

        await crud.update_submenu(menu_id, submenu_id, patch, self.db)
        updated_submenu = await crud.read_submenu(menu_id, submenu_id, self.db)
        await set_cache("submenu", submenu_id, updated_submenu)
        # чистим кэш получения списка подменю
        await clear_cache("submenu", "all")
        return updated_submenu

    async def delete(self, menu_id: str, submenu_id: str) -> Message:
        """Удалить подменю."""

        if not await crud.read_submenu(menu_id, submenu_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="submenu not found",
            )

        await crud.delete_submenu(menu_id, submenu_id, self.db)
        await clear_cache("submenu", submenu_id)
        # Чистим кэш для родительских элементов и получения списков элементов
        await clear_cache("submenu", "all")
        await clear_cache("menu", menu_id)
        await clear_cache("menu", "all")
        return Message(status=True, message="The submenu has been deleted")


def get_submenu_service(db: AsyncSession = Depends(get_db)) -> SubmenuService:
    return SubmenuService(db=db)
