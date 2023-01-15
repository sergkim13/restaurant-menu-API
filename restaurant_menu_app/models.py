from sqlalchemy import (
    Column, MetaData, BigInteger, String, ForeignKey, Identity, Float)
from sqlalchemy.orm import relationship

from .database import Base

metadata = MetaData()


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(BigInteger, Identity(always=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    menu_submenus = relationship("Submenu", back_populates="main_menu")


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(BigInteger, Identity(always=True), primary_key=True)
    menu_id = Column(BigInteger, ForeignKey("menus.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    main_menu = relationship("Menu", back_populates="menu_submenus")
    submenu_dishes = relationship("Dish", back_populates="submenu")


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(BigInteger, Identity(always=True), primary_key=True)
    submenu_id = Column(BigInteger, ForeignKey("submenus.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float)

    submenu = relationship("Submenu", back_populates="submenu_dishes")




# menu = Table(
#     "menus",
#     metadata,
#     Column("id", BigInteger, Identity(always=True), primary_key=True),
#     Column("title", String, nullable=False),
#     Column("description", String, nullable=False),
# )

# submenu = Table(
#     "submenus",
#     metadata,
#     Column("id", BigInteger, Identity(always=True), primary_key=True),
#     Column("menu_id", BigInteger, ForeignKey(menu.c.id)),
#     Column("title", String, nullable=False),
#     Column("description", String, nullable=False),
# )

# dish = Table(
#     "dishes",
#     metadata,
#     Column("id", BigInteger, Identity(always=True), primary_key=True),
#     Column("submenu_id", BigInteger, ForeignKey(submenu.c.id)),
#     Column("title", String, nullable=False),
#     Column("description", String, nullable=False),
#     Column("price", Float),
# )
