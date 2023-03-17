import uuid
from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str


class ShopCreate(BaseModel):
    name: str

class UserUpdate(schemas.BaseUserUpdate):
    pass

