from pydantic import BaseModel
from typing import List


class UserInfoBase(BaseModel):
    username: str
    fullname: str


class UserCreate(UserInfoBase):
    password: str


class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True


class UserAuthenticate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
