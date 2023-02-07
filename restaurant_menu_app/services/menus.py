from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.db.cache.abstract_cache import AbstractCache
from restaurant_menu_app.db.cache.cache_operations import get_cache
from restaurant_menu_app.db.main_db.crud.abstract_crud import AbstractCRUD
from restaurant_menu_app.db.main_db.crud.menus import MenuCRUD
from restaurant_menu_app.db.main_db.database import get_db
from restaurant_menu_app.schemas.scheme import MenuCreate, MenuInfo, MenuUpdate, Message


class MenuService:
    def __init__(self, menu_crud: AbstractCRUD, cache: AbstractCache) -> None:
        self.menu_crud = menu_crud
        self.cache = cache

    async def get_list(self) -> list[MenuInfo]:
        """Получить список меню."""

        if await self.cache.is_cached("menus"):
            return await self.cache.get("menus")

        menus = await self.menu_crud.read_all()
        await self.cache.set("menus", menus)
        return menus

    async def get_info(self, menu_id: str) -> MenuInfo:
        """Получить информацию о меню."""

        if await self.cache.is_cached(menu_id):
            return await self.cache.get(menu_id)

        menu = await self.menu_crud.read(menu_id)
        if not menu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="menu not found",
            )
        await self.cache.set(menu_id, menu)
        return menu

    async def create(self, data: MenuCreate) -> MenuInfo:
        """Cоздать меню."""

        try:
            new_menu = await self.menu_crud.create(data)
        except IntegrityError as e:
            if "UniqueViolationError" in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Menu with that title already exists",
                )
            else:
                raise

        created_menu = await self.menu_crud.read(new_menu.id)
        await self.cache.set(str(created_menu.id), created_menu)
        await self.cache.clear("menus")
        return created_menu

    async def update(self, menu_id: str, patch: MenuUpdate) -> MenuInfo:
        """Обновить меню."""

        if not await self.menu_crud.read(menu_id):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="menu not found",
            )

        await self.menu_crud.update(menu_id, patch)
        updated_menu = await self.menu_crud.read(menu_id)
        await self.cache.set(menu_id, updated_menu)
        await self.cache.clear("menus")
        return updated_menu

    async def delete(self, menu_id: str) -> Message:
        """Удалить меню."""

        if not await self.menu_crud.read(menu_id):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="menu not found",
            )

        await self.menu_crud.delete(menu_id)
        await self.cache.clear(menu_id)
        await self.cache.clear("menus")
        return Message(status=True, message="The menu has been deleted")


def get_menu_service(
    db: AsyncSession = Depends(get_db),
    cache: AbstractCache = Depends(get_cache),
) -> MenuService:
    menu_crud = MenuCRUD(db=db)
    return MenuService(menu_crud=menu_crud, cache=cache)
