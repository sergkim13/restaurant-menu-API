from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_menu_app.models import model


async def get_all(db: AsyncSession):
    query = select(
        func.json_agg(
            func.json_build_object(
                "menu_id",
                model.Menu.id,
                "menu_title",
                model.Menu.title,
                "menu_description",
                model.Menu.description,
                "child_submenus",
                select(
                    func.json_agg(
                        func.json_build_object(
                            "submenu_id",
                            model.Submenu.id,
                            "submenu_title",
                            model.Submenu.title,
                            "submenu_description",
                            model.Submenu.description,
                            "child_dishes",
                            select(
                                func.json_agg(
                                    func.json_build_object(
                                        "dish_id",
                                        model.Dish.id,
                                        "dish_title",
                                        model.Dish.title,
                                        "dish_description",
                                        model.Dish.description,
                                        "dish_price",
                                        model.Dish.price,
                                    )
                                )
                            ).where(model.Dish.submenu_id == model.Submenu.id),
                        )
                    )
                ).where(model.Submenu.menu_id == model.Menu.id),
            )
        )
    )
    print(query)
    query_result = await db.execute(query)
    result = jsonable_encoder(query_result.first())["json_agg"]
    return result
