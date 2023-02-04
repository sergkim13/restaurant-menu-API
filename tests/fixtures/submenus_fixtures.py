import uuid

fake_id = uuid.uuid4()
new_submenu = {"title": "Soups", "description": "just soups"}
upd_submenu = {"title": "Updated soups", "description": "brand new soups"}
submenu_not_found = {"detail": "submenu not found"}
submenu_deleted = {"status": True, "message": "The submenu has been deleted"}
