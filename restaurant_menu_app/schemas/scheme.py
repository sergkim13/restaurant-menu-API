from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, validator


# Menu schemas
class MenuBase(BaseModel):
    title: str
    description: str


class MenuInfo(MenuBase):
    id: UUID4 = Field(default_factory=uuid4)
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': '4a89f97a-c1e0-49a4-8f72-41934ed63439',
                'title': 'My menu',
                'description': 'My menu description',
                'submenus_count': 7,
                'dishes_count': 77,
            },
        }


class MenuCreate(MenuBase):
    pass

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'My new menu',
                'description': 'My new menu description',
            },
        }


class MenuUpdate(BaseModel):
    title: str | None
    description: str | None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'My updated menu',
                'description': 'My updated menu description',
            },
        }


# Sunmenu schemas
class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuInfo(SubmenuBase):
    id: UUID4 = Field(default_factory=uuid4)
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': '4a89f97a-c1e0-49a4-8f72-41934ed63439',
                'title': 'My submenu',
                'description': 'My submenu description',
                'dishes_count': 8,
            },
        }


class SubmenuCreate(SubmenuBase):
    pass

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'My new submenu',
                'description': 'My new submenu description',
            },
        }


class SubmenuUpdate(BaseModel):
    title: str | None
    description: str | None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'My updated submenu',
                'description': 'My updated submenu description',
            },
        }


# Dishes schemas
class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishInfo(DishBase):
    id: UUID4 = Field(default_factory=uuid4)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': '4a89f97a-c1e0-49a4-8f72-41934ed63439',
                'title': 'My dish',
                'description': 'My dish description',
                'price': '90.00',
            },
        }

    @validator('price')
    def normalize_price(cls, price):
        return f'{price:0.2f}'


class DishCreate(DishBase):
    pass

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'My new dish',
                'description': 'My new dish description',
                'price': 90,
            },
        }


class DishUpdate(BaseModel):
    title: str | None
    description: str | None
    price: float | None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'My updated dish',
                'description': 'My updated dish description',
                'price': 90,
            },
        }


class Message(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True
