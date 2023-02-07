import uuid

from sqlalchemy import Column, Float, ForeignKey, MetaData, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from restaurant_menu_app.db.main_db.database import Base

metadata = MetaData()


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

    menu_submenus = relationship(
        "Submenu",
        cascade="save-update, merge, delete",
        passive_deletes=True,
        back_populates="main_menu",
    )


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    menu_id = Column(
        ForeignKey("menus.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    main_menu = relationship("Menu", back_populates="menu_submenus")
    submenu_dishes = relationship(
        "Dish",
        cascade="save-update, merge, delete",
        passive_deletes=True,
        back_populates="submenu",
    )

    __table_args__ = (
        UniqueConstraint(
            "menu_id",
            "title",
            name="_menu_submenu_uc",
        ),
    )


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submenu_id = Column(
        ForeignKey("submenus.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float)

    submenu = relationship("Submenu", back_populates="submenu_dishes")

    __table_args__ = (
        UniqueConstraint(
            "submenu_id",
            "title",
            name="_submenu_dish_uc",
        ),
    )
