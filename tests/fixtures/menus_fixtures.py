import uuid

fake_id = uuid.uuid4()
new_menu = {"title": "Main menu", "description": "our main menu"}
upd_menu = {"title": "Updated menu", "description": "our updated main menu"}
menu_not_found = {"detail": "menu not found"}
menu_deleted = {"status": True, "message": "The menu has been deleted"}
