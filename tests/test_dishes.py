from http import HTTPStatus

import pytest

from tests.fixtures.dishes_fixtures import (
    dish_deleted,
    dish_not_found,
    fake_id,
    new_dish,
    upd_dish,
)


@pytest.mark.asyncio
async def test_get_empty_dishes(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]["id"])

    response = await client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_dish(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]["id"])
    dish_title = new_dish["title"]
    dish_description = new_dish["description"]
    dish_price = "{:0.2f}".format(new_dish["price"])

    response = await client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json=new_dish,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert "id" in response.json()
    assert response.json()["title"] == dish_title
    assert response.json()["description"] == dish_description
    assert response.json()["price"] == dish_price


@pytest.mark.asyncio
async def test_get_dishes(fixture_dish, client):
    menu_id = str(fixture_dish[0])
    submenu_id = str(fixture_dish[1])

    response = await client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_dish(fixture_dish, client):
    menu_id = str(fixture_dish[0])
    submenu_id = str(fixture_dish[1])
    dish_id = str(fixture_dish[2].id)
    dish_title = fixture_dish[2].title
    dish_description = fixture_dish[2].description
    dish_price = f"{fixture_dish[2].price:0.2f}"

    response = await client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == dish_id
    assert response.json()["title"] == dish_title
    assert response.json()["description"] == dish_description
    assert response.json()["price"] == dish_price


@pytest.mark.asyncio
async def test_get_dish_not_found(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]["id"])

    response = await client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{fake_id}",
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == dish_not_found


@pytest.mark.asyncio
async def test_patch_dish(fixture_dish, client):
    menu_id = str(fixture_dish[0])
    submenu_id = str(fixture_dish[1])
    dish_id = str(fixture_dish[2].id)
    dish_title = upd_dish["title"]
    dish_description = upd_dish["description"]
    dish_price = "{:0.2f}".format(upd_dish["price"])

    response = await client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json=upd_dish,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == dish_id
    assert response.json()["title"] == dish_title
    assert response.json()["description"] == dish_description
    assert response.json()["price"] == dish_price


@pytest.mark.asyncio
async def test_delete_dish(fixture_dish, client):
    menu_id = str(fixture_dish[0])
    submenu_id = str(fixture_dish[1])
    dish_id = str(fixture_dish[2].id)

    response = await client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == dish_deleted
    response_after_delete = await client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    )
    assert response_after_delete.status_code == HTTPStatus.NOT_FOUND
