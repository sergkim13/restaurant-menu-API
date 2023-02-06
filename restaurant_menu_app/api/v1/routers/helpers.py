from http import HTTPStatus

from fastapi import APIRouter, Depends

from restaurant_menu_app.schemas.scheme import Message
from restaurant_menu_app.services.helper import HelperServise, get_helper_service

router = APIRouter(
    prefix="/api/v1",
    tags=["Helpers"],
)


@router.post(
    path="/generated_test_data",
    response_model=Message,
    summary="Генерация тестовых данных",
    status_code=HTTPStatus.CREATED,
)
async def generate_data(
    helper_service: HelperServise = Depends(get_helper_service),
) -> Message:
    return await helper_service.generate_test_data()


@router.post(
    path="/content_as_file",
    summary="Создание задачи на получение всех данных в excel-файле",
    status_code=HTTPStatus.ACCEPTED,
)
async def create_file_with_full_content(helper_service: HelperServise = Depends(get_helper_service)):
    return await helper_service.put_all_data_to_file()


@router.get(
    path="/content_as_file/{task_id}",
    summary="Получение резльутата задачи на получение всех данных в excel-файле",
    status_code=HTTPStatus.OK,
)
async def get_file_with_full_content(task_id: str, helper_service: HelperServise = Depends(get_helper_service)):
    return helper_service.get_all_data_in_file(task_id)
