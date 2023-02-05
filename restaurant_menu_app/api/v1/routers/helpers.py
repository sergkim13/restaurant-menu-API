from http import HTTPStatus

from fastapi import APIRouter, Depends

from restaurant_menu_app.schemas.scheme import Message
from restaurant_menu_app.services.data_generator import (
    DataGeneratorService,
    get_data_generator_service,
)
from restaurant_menu_app.services.tasks import TaskServise, get_task_service

router = APIRouter(
    prefix="/api/v1",
    tags=["Helpers"],
)


@router.post(
    path="/generated_data",
    response_model=Message,
    summary="Генерация тестовых данных",
    status_code=HTTPStatus.CREATED,
)
async def generate_data(
    data_generator: DataGeneratorService = Depends(get_data_generator_service),
) -> Message:
    return await data_generator.generate()


@router.post(
    path="/content_as_file",
    summary="Создание задачи на получение всех данных в excel-файле",
    status_code=HTTPStatus.ACCEPTED,
)
async def create_file_with_full_content(task_service: TaskServise = Depends(get_task_service)):
    return await task_service.task_to_download_all_data()


@router.get(
    path="/content_as_file/{task_id}",
    summary="Получение резльутата задачи на получение всех данных в excel-файле",
    status_code=HTTPStatus.OK,
)
async def get_file_with_full_content(task_id: str, task_service: TaskServise = Depends(get_task_service)):
    return task_service.get_task_result(task_id)
