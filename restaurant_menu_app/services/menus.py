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
from restaurant_menu_app.schemas.scheme import MenuCreate, MenuInfo, MenuUpdate, Message


class MenuService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self) -> list[MenuInfo]:
        """Получить список меню."""

        if await is_cached("menu", "all"):
            return await get_cache("menu", "all")

        menus = await crud.read_menus(self.db)
        await set_cache("menu", "all", menus)
        return menus

    async def get_info(self, menu_id: str) -> MenuInfo:
        """Получить информацию о меню."""

        if await is_cached("menu", menu_id):
            return await get_cache("menu", menu_id)

        menu = await crud.read_menu(menu_id, self.db)
        if not menu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="menu not found",
            )
        await set_cache("menu", menu_id, menu)
        return menu

    async def create(self, data: MenuCreate) -> MenuInfo:
        """Cоздать меню."""

        try:
            new_menu = await crud.create_menu(data, self.db)
        except IntegrityError as e:
            if "UniqueViolationError" in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Menu with that title already exists",
                )
            else:
                raise

        created_menu = await crud.read_menu(new_menu.id, self.db)
        await set_cache("menu", new_menu.id, created_menu)
        await clear_cache("menu", "all")  # чистим кэш получения списка меню
        return created_menu

    async def update(self, menu_id: str, patch: MenuUpdate) -> MenuInfo:
        """Обновить меню."""

        if not await crud.read_menu(menu_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="menu not found",
            )

        await crud.update_menu(menu_id, patch, self.db)
        updated_menu = await crud.read_menu(menu_id, self.db)
        await set_cache("menu", menu_id, updated_menu)
        await clear_cache("menu", "all")  # чистим кэш получения списка меню
        return updated_menu

    async def delete(self, menu_id: str) -> Message:
        """Удалить меню."""

        if not await crud.read_menu(menu_id, self.db):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="menu not found",
            )

        await crud.delete_menu(menu_id, self.db)
        await clear_cache("menu", menu_id)
        await clear_cache("menu", "all")  # чистим кэш получения списка меню
        return Message(status=True, message="The menu has been deleted")


def get_menu_service(db: AsyncSession = Depends(get_db)) -> MenuService:
    return MenuService(db=db)
