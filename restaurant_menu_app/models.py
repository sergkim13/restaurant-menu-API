from sqlalchemy import (
    Column, MetaData, BigInteger, String, ForeignKey, Identity, Float, UniqueConstraint)
from sqlalchemy.orm import relationship

from .database import Base

metadata = MetaData()


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(BigInteger, Identity(always=True), primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

    menu_submenus = relationship(
        "Submenu", cascade="all, delete", back_populates="main_menu")


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(BigInteger, Identity(always=True), primary_key=True)
    menu_id = Column(BigInteger, ForeignKey("menus.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    main_menu = relationship("Menu", back_populates="menu_submenus")
    submenu_dishes = relationship(
        "Dish", cascade="all, delete", back_populates="submenu")

    __table_args__ = (
        UniqueConstraint("menu_id", "title", name='_menu_submenu_uc'),)


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(BigInteger, Identity(always=True), primary_key=True)
    submenu_id = Column(BigInteger, ForeignKey("submenus.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float)

    submenu = relationship("Submenu", back_populates="submenu_dishes")

    __table_args__ = (
        UniqueConstraint("submenu_id", "title", name='_submenu_dish_uc'),)
