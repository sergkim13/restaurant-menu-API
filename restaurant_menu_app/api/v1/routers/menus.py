from http import HTTPStatus

from fastapi import APIRouter, Depends

from restaurant_menu_app.schemas.scheme import MenuCreate, MenuInfo, MenuUpdate, Message
from restaurant_menu_app.services.menus import MenuService, get_menu_service

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['Menus'],
)


@router.get(
    path='',
    response_model=list[MenuInfo],
    summary='Получение списка всех меню',
    status_code=HTTPStatus.OK,
)
async def get_menus(
    menu_service: MenuService = Depends(get_menu_service),
) -> list[MenuInfo]:
    return await menu_service.get_list()


@router.get(
    path='/{menu_id}',
    response_model=MenuInfo,
    summary='Получение информации о меню',
    status_code=HTTPStatus.OK,
)
async def get_menu(
    menu_id: str,
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuInfo:
    return await menu_service.get_info(menu_id)


@router.post(
    path='',
    response_model=MenuInfo,
    summary='Создание меню',
    status_code=HTTPStatus.CREATED,
)
async def post_menu(
    new_menu: MenuCreate,
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuInfo:
    return await menu_service.create(new_menu)


@router.patch(
    path='/{menu_id}',
    response_model=MenuInfo,
    summary='Обновление меню',
    status_code=HTTPStatus.OK,
)
async def patch_menu(
    menu_id: str,
    patch: MenuUpdate,
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuInfo:
    return await menu_service.update(menu_id, patch)


@router.delete(
    path='/{menu_id}',
    response_model=Message,
    summary='Удаление меню',
    status_code=HTTPStatus.OK,
)
async def delete_menu(
    menu_id: str,
    menu_service: MenuService = Depends(get_menu_service),
) -> Message:
    return await menu_service.delete(menu_id)
