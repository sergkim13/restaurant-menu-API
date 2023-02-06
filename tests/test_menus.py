from http import HTTPStatus

import pytest

from tests.fixtures.menus_fixtures import (
    fake_id,
    menu_deleted,
    menu_not_found,
    new_menu,
    upd_menu,
)


@pytest.mark.asyncio
async def test_get_empty_menus(client):
    response = await client.get("/api/v1/menus")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_menu(client):
    response = await client.post("/api/v1/menus", json=new_menu)
    assert response.status_code == HTTPStatus.CREATED
    assert "id" in response.json()
    assert response.json()["title"] == new_menu["title"]
    assert response.json()["description"] == new_menu["description"]
    assert response.json()["submenus_count"] == 0
    assert response.json()["dishes_count"] == 0


@pytest.mark.asyncio
async def test_get_menus(fixture_menu, client):
    menu_id = str(fixture_menu["id"])

    response = await client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json()[0]["id"] == menu_id
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_menu(fixture_menu, client):
    menu_id = str(fixture_menu["id"])
    menu_title = fixture_menu["title"]
    menu_description = fixture_menu["description"]

    response = await client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == menu_title
    assert response.json()["description"] == menu_description


@pytest.mark.asyncio
async def test_get_menu_not_found(client):
    response = await client.get(f"/api/v1/menus/{fake_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == menu_not_found


@pytest.mark.asyncio
async def test_patch_menu(fixture_menu, client):
    menu_id = str(fixture_menu["id"])
    menu_title = upd_menu["title"]
    menu_description = upd_menu["description"]

    response = await client.patch(f"/api/v1/menus/{menu_id}", json=upd_menu)
    assert response.status_code == HTTPStatus.OK
    assert "id" in response.json()
    assert response.json()["title"] == menu_title
    assert response.json()["description"] == menu_description


@pytest.mark.asyncio
async def test_delete_menu(fixture_menu, client):
    menu_id = str(fixture_menu["id"])

    response = await client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == menu_deleted
    response_after_delete = await client.get(f"/api/v1/menus/{menu_id}")
    assert response_after_delete.status_code == HTTPStatus.NOT_FOUND
