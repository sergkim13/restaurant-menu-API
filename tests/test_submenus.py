import pytest

from tests.fixtures.submenus_fixtures import (
    fake_id,
    new_submenu,
    submenu_deleted,
    submenu_not_found,
    upd_submenu,
)


@pytest.mark.asyncio
async def test_get_empty_submenus(fixture_menu, client):
    menu_id = str(fixture_menu["id"])

    response = await client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_submenu(fixture_menu, client):
    menu_id = str(fixture_menu["id"])
    submenu_title = new_submenu["title"]
    submenu_description = new_submenu["description"]

    response = await client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json=new_submenu,
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == submenu_title
    assert response.json()["description"] == submenu_description
    assert response.json()["dishes_count"] == 0


@pytest.mark.asyncio
async def test_get_submenus(fixture_submenu, client):
    menu_id = fixture_submenu[0]

    response = await client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_submenu(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]["id"])
    submenu_title = fixture_submenu[1]["title"]
    submenu_description = fixture_submenu[1]["description"]

    response = await client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()["title"] == submenu_title
    assert response.json()["description"] == submenu_description
    assert response.json()["dishes_count"] == 0


@pytest.mark.asyncio
async def test_get_submenu_not_found(fixture_menu, client):
    menu_id = fixture_menu["id"]

    response = await client.get(f"/api/v1/menus/{menu_id}/submenus/{fake_id}")
    assert response.status_code == 404
    assert response.json() == submenu_not_found


@pytest.mark.asyncio
async def test_patch_submenu(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]["id"])
    submenu_title = upd_submenu["title"]
    submenu_description = upd_submenu["description"]

    response = await client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        json=upd_submenu,
    )
    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()["title"] == submenu_title
    assert response.json()["description"] == submenu_description
    assert response.json()["dishes_count"] == 0


@pytest.mark.asyncio
async def test_delete_submenu(fixture_submenu, client):
    menu_id = fixture_submenu[0]
    submenu_id = fixture_submenu[1]["id"]

    response = await client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == submenu_deleted
    response_after_delete = await client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    )
    assert response_after_delete.status_code == 404
