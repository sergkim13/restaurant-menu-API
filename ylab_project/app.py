from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def home():
    return 'Welcome to our restaurant!'


@app.get('/api/v1/menus')
def get_menus():
    pass


@app.get('/api/v1/menus/{menu_id}')
def get_menu(menu_id):
    pass


@app.post('/api/v1/menus')
def post_menu():
    pass


@app.patch('/api/v1/menus/{menu_id}')
def patch_menu(menu_id):
    pass


@app.delete('/app/v1/menus/{menu_id}')
def delete_menu(menu_id):
    pass


@app.get('/api/v1/menus/{menu_id}/submenus')
def get_submenus(menu_id):
    pass


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def get_submenu(menu_id, submenu_id):
    pass


@app.post('/api/v1/menus/{menu_id}/submenus')
def post_submenu(menu_id):
    pass


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def patch_submenu(menu_id, submenu_id):
    pass


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id, submenu_id):
    pass


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def get_dishes(menu_id, submenu_id):
    pass


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def get_dish(menu_id, submenu_id, dish_id):
    pass


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def post_dish(menu_id, submenu_id):
    pass


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id, submenu_id, dish_id):
    pass
