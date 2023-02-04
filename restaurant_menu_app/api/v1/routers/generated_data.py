from http import HTTPStatus

from fastapi import APIRouter, Depends

from restaurant_menu_app.schemas.scheme import Message
from restaurant_menu_app.services.data_generator import (
    DataGeneratorService,
    get_data_generator_service,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["Autogenerate data"],
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
