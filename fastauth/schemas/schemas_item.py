from fastauth.db.database import Base
from pydantic import BaseModel
from typing import List

from sqlalchemy import Integer


class ItemsCreate(BaseModel):
    item_name: str
    item_type: str
    owner_id: int


class ItemsDisplay(BaseModel):
    id: int
    item_name: str
    item_type: str
    owner_id: int


class ItemsUpdate(BaseModel):
    item_name: str
    item_type: str


class ItemInfo(ItemsCreate):
    id: int

    class Config:
        orm_mode = True
