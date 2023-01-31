import pytest

from restaurant_menu_app.db.cache.cache_settings import redis_client
from restaurant_menu_app.db.main_db import crud
from restaurant_menu_app.schemas import scheme

# Data fixtures
new_menu = {'title': 'Main menu', 'description': 'our main menu'}
upd_menu = {'title': 'Updated menu', 'description': 'our updated main menu'}

new_submenu = {'title': 'Soups', 'description': 'just soups'}
upd_submenu = {'title': 'Updated soups', 'description': 'brand new soups'}

new_dish = {'title': 'Borsh', 'description': 'best borsh', 'price': 300}
upd_dish = {
    'title': 'Updated borsh',
    'description': 'brand new borsh', 'price': 450,
}

menu_not_found = {'detail': 'menu not found'}
menu_deleted = {'status': True, 'message': 'The menu has been deleted'}
submenu_not_found = {'detail': 'submenu not found'}
submenu_deleted = {'status': True, 'message': 'The submenu has been deleted'}
dish_not_found = {'detail': 'dish not found'}
dish_deleted = {'status': True, 'message': 'The dish has been deleted'}


@pytest.fixture(scope='function', autouse=True)
def clear_cache():
    redis_client.flushdb()


# CRUD fixtures
@pytest.fixture
def fixture_menu(db):
    menu = crud.create_menu(scheme.MenuCreate(**new_menu), db)
    return crud.read_menu(menu.id, db)


@pytest.fixture
def fixture_submenu(db, fixture_menu):
    menu = fixture_menu
    submenu = crud.create_submenu(
        menu.id, scheme.SubmenuCreate(**new_submenu), db,
    )
    return menu.id, crud.read_submenu(menu.id, submenu.id, db)


@pytest.fixture
def fixture_dish(db, fixture_menu, fixture_submenu):
    menu = fixture_menu
    submenu = fixture_submenu[1]
    dish = crud.create_dish(submenu.id, scheme.DishCreate(**new_dish), db)
    return menu.id, submenu.id, crud.read_dish(menu.id, submenu.id, dish.id, db)


def test_get_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == 'Welcome to our restaurant!'


# Menus tests
def test_get_empty_menus(client):
    response = client.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []


def test_post_menu(client):
    response = client.post('/api/v1/menus', json=new_menu)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == new_menu['title']
    assert response.json()['description'] == new_menu['description']
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


def test_get_menus(fixture_menu, client):
    menu_id = str(fixture_menu['id'])

    response = client.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json()[0]['id'] == menu_id
    assert len(response.json()) == 1


def test_get_menu(fixture_menu, client):
    menu_id = str(fixture_menu['id'])
    menu_title = fixture_menu['title']
    menu_description = fixture_menu['description']

    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == menu_id
    assert response.json()['title'] == menu_title
    assert response.json()['description'] == menu_description


def test_get_menu_not_found(client):
    response = client.get('/api/v1/menus/1')
    assert response.status_code == 404
    assert response.json() == menu_not_found


def test_patch_menu(fixture_menu, client):
    menu_id = str(fixture_menu['id'])
    menu_title = upd_menu['title']
    menu_description = upd_menu['description']

    response = client.patch(f'/api/v1/menus/{menu_id}', json=upd_menu)
    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()['title'] == menu_title
    assert response.json()['description'] == menu_description


def test_delete_menu(fixture_menu, client):
    menu_id = str(fixture_menu['id'])

    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json() == menu_deleted
    assert client.get(f'/api/v1/menus/{menu_id}').status_code == 404


# Submenus tests
def test_get_empty_submenus(fixture_menu, client):
    menu_id = str(fixture_menu['id'])

    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == []


def test_post_submenu(fixture_menu, client):
    menu_id = str(fixture_menu['id'])
    submenu_title = new_submenu['title']
    submenu_description = new_submenu['description']

    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus', json=new_submenu,
    )
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == submenu_title
    assert response.json()['description'] == submenu_description
    assert response.json()['dishes_count'] == 0


def test_get_submenus(fixture_submenu, client):
    menu_id = fixture_submenu[0]

    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_submenu(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]['id'])
    submenu_title = fixture_submenu[1]['title']
    submenu_description = fixture_submenu[1]['description']

    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == submenu_id
    assert response.json()['title'] == submenu_title
    assert response.json()['description'] == submenu_description
    assert response.json()['dishes_count'] == 0


def test_get_submenu_not_found(fixture_menu, client):
    menu_id = fixture_menu['id']

    response = client.get(f'/api/v1/menus/{menu_id}/submenus/666')
    assert response.status_code == 404
    assert response.json() == submenu_not_found


def test_patch_submenu(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]['id'])
    submenu_title = upd_submenu['title']
    submenu_description = upd_submenu['description']

    response = client.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json=upd_submenu,
    )
    assert response.status_code == 200
    assert response.json()['id'] == submenu_id
    assert response.json()['title'] == submenu_title
    assert response.json()['description'] == submenu_description
    assert response.json()['dishes_count'] == 0


def test_delete_submenu(fixture_submenu, client):
    menu_id = fixture_submenu[0]
    submenu_id = fixture_submenu[1]['id']

    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json() == submenu_deleted
    assert client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    ).status_code == 404


# Dishes tests
def test_get_empty_dishes(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]['id'])

    response = client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    )
    assert response.status_code == 200
    assert response.json() == []


def test_post_dish(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]['id'])
    dish_title = new_dish['title']
    dish_description = new_dish['description']
    dish_price = '{:0.2f}'.format(new_dish['price'])

    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=new_dish,
    )
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == dish_title
    assert response.json()['description'] == dish_description
    assert response.json()['price'] == dish_price


def test_get_dishes(fixture_dish, client):
    menu_id = str(fixture_dish[0])
    submenu_id = str(fixture_dish[1])

    response = client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_dish(fixture_dish, client):
    menu_id = str(fixture_dish[0])
    submenu_id = str(fixture_dish[1])
    dish_id = str(fixture_dish[2].id)
    dish_title = fixture_dish[2].title
    dish_description = fixture_dish[2].description
    dish_price = f'{fixture_dish[2].price:0.2f}'

    response = client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    )
    assert response.status_code == 200
    assert response.json()['id'] == dish_id
    assert response.json()['title'] == dish_title
    assert response.json()['description'] == dish_description
    assert response.json()['price'] == dish_price


def test_get_dish_not_found(fixture_submenu, client):
    menu_id = str(fixture_submenu[0])
    submenu_id = str(fixture_submenu[1]['id'])

    response = client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/666',
    )
    assert response.status_code == 404
    assert response.json() == dish_not_found


def test_patch_dish(fixture_dish, client):
    menu_id = str(fixture_dish[0])
    submenu_id = str(fixture_dish[1])
    dish_id = str(fixture_dish[2].id)
    dish_title = upd_dish['title']
    dish_description = upd_dish['description']
    dish_price = '{:0.2f}'.format(upd_dish['price'])

    response = client.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=upd_dish,
    )
    assert response.status_code == 200
    assert response.json()['id'] == dish_id
    assert response.json()['title'] == dish_title
    assert response.json()['description'] == dish_description
    assert response.json()['price'] == dish_price


def test_delete_dish(fixture_dish, client):
    menu_id = str(fixture_dish[0])
    submenu_id = str(fixture_dish[1])
    dish_id = str(fixture_dish[2].id)

    response = client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    )
    assert response.status_code == 200
    assert response.json() == dish_deleted
    assert client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    ).status_code == 404
