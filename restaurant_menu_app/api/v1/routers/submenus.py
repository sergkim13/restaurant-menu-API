from http import HTTPStatus

from fastapi import APIRouter, Depends

from restaurant_menu_app.schemas.scheme import (
    Message,
    SubmenuCreate,
    SubmenuInfo,
    SubmenuUpdate,
)
from restaurant_menu_app.services.submenus import SubmenuService, get_submenu_service

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['Submenus'],
)


@router.get(
    path='',
    response_model=list[SubmenuInfo],
    summary='Просмотр списка подменю',
    status_code=HTTPStatus.OK,
)
async def get_submenus(
    menu_id: str,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> list[SubmenuInfo]:
    return await submenu_service.get_list(menu_id)


@router.get(
    path='/{submenu_id}',
    response_model=SubmenuInfo,
    summary='Просмотр информации о подменю',
    status_code=HTTPStatus.OK,
)
async def get_submenu(
    menu_id: str,
    submenu_id: str,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuInfo:
    return await submenu_service.get_info(menu_id, submenu_id)


@router.post(
    path='',
    response_model=SubmenuInfo,
    summary='Создание подменю',
    status_code=HTTPStatus.CREATED,
)
async def post_submenu(
    menu_id: str,
    new_submenu: SubmenuCreate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuInfo:

    return await submenu_service.create(menu_id, new_submenu)


@router.patch(
    path='/{submenu_id}',
    response_model=SubmenuInfo,
    summary='Обновление подменю',
    status_code=HTTPStatus.OK,
)
async def patch_submenu(
    menu_id: str,
    submenu_id: str,
    patch: SubmenuUpdate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuInfo:
    return await submenu_service.update(menu_id, submenu_id, patch)


@router.delete(
    path='/{submenu_id}',
    response_model=Message,
    summary='Удаление подменю',
    status_code=HTTPStatus.OK,
)
async def delete_submenu(
    menu_id: str,
    submenu_id: str,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> Message:
    return await submenu_service.delete(menu_id, submenu_id)
