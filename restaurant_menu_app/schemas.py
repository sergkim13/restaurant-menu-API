from pydantic import BaseModel


class MenuInfo(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class MenuCreate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuUpdate(MenuCreate):
    pass

    class Config:
        orm_mode = True


class SubmenuInfo(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuCreate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SubmenuUpdate(SubmenuCreate):
    pass

    class Config:
        orm_mode = True


class DishInfo(BaseModel):
    id: str
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishCreate(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


class DishUpdate(DishCreate):
    pass

    class Config:
        orm_mode = True


class Message(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True
