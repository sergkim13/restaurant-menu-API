from pydantic import BaseModel


class MenuInfo(BaseModel):
    id: str
    title: str
    description: str

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


class Message(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True

