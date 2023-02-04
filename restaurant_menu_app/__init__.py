from .models.model import Menu, Submenu, Dish
from .db.main_db.database import Base

__all__ = ["Base", "Menu", "Submenu", "Dish"]
