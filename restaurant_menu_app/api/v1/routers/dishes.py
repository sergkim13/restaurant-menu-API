from http import HTTPStatus

from fastapi import APIRouter, Depends

from restaurant_menu_app.schemas.scheme import DishCreate, DishInfo, DishUpdate, Message
from restaurant_menu_app.services.dishes import DishService, get_dish_service

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"],
)


@router.get(
    path="",
    response_model=list[DishInfo],
    summary="Просмотр списка блюд",
    status_code=HTTPStatus.OK,
)
async def get_dishes(
    menu_id: str,
    submenu_id: str,
    dish_service: DishService = Depends(get_dish_service),
) -> list[DishInfo]:
    return await dish_service.get_list(menu_id, submenu_id)


@router.get(
    path="/{dish_id}",
    response_model=DishInfo,
    summary="Просмотр информации о блюде",
    status_code=HTTPStatus.OK,
)
async def get_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish_service: DishService = Depends(get_dish_service),
) -> DishInfo:
    return await dish_service.get_info(menu_id, submenu_id, dish_id)


@router.post(
    path="",
    response_model=DishInfo,
    summary="Создание блюда",
    status_code=HTTPStatus.CREATED,
)
async def post_dish(
    menu_id: str,
    submenu_id: str,
    new_dish: DishCreate,
    dish_service: DishService = Depends(get_dish_service),
) -> DishInfo:
    return await dish_service.create(menu_id, submenu_id, new_dish)


@router.patch(
    path="/{dish_id}",
    response_model=DishInfo,
    summary="Обновление блюда",
    status_code=HTTPStatus.OK,
)
async def patch_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    patch: DishUpdate,
    dish_service: DishService = Depends(get_dish_service),
) -> DishInfo:
    return await dish_service.update(menu_id, submenu_id, dish_id, patch)


@router.delete(
    path="/{dish_id}",
    response_model=Message,
    summary="Удаление блюда",
    status_code=HTTPStatus.OK,
)
async def delete_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish_service: DishService = Depends(get_dish_service),
) -> Message:
    return await dish_service.delete(menu_id, submenu_id, dish_id)
