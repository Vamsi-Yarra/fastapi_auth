from turtle import onclick
from fastapi import APIRouter, Depends, HTTPException, status
from tomlkit import item
from fastauth.auth import auth
from fastauth.crud import crud_item, crud_user
from ..schemas import schemas_item
from sqlalchemy.orm import Session
from fastauth.dependencies import get_db

item_router = APIRouter()

UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='You are not the Owner of the Item',
)

INVALID_OWNER_ID = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='You have entered an invalid Owner Item',
)


@item_router.post('/item', status_code=201, tags=['ITEMS'])
def create_item(new_item: schemas_item.ItemsCreate, db: Session = Depends(get_db)):
    return crud_item.create_item(db, new_item)


@item_router.put('/item/{item_id}', status_code=200, tags=['ITEMS'])
def update_item(item_id: int, token: str, update_item: schemas_item.ItemsUpdate, db: Session = Depends(get_db)):
    owner = get_owner(db, token)
    item = crud_item.get_item_by_item_id(db, item_id)
    if owner.id == item.owner_id:
        return crud_item.update_item(db, item_id, update_item)
    else:
        raise UNAUTHORIZED_EXCEPTION


@item_router.get('/item/{item_id}', status_code=200, tags=['ITEMS'])
def get_item(item_id: int, db: Session = Depends(get_db)):
    return crud_item.get_item_by_item_id(db, item_id)


@item_router.delete('/item/{item_id}', status_code=200, tags=['ITEMS'])
def delete_item(item_id: int, token: str, db: Session = Depends(get_db)):
    owner = get_owner(db, token)
    item = crud_item.get_item_by_item_id(db, item_id)
    if owner.id == item.owner_id:
        return crud_item.delete_item(db, item_id)
    else:
        raise UNAUTHORIZED_EXCEPTION


def get_owner(db: Session, token: str):
    owner_name = auth.decode_jwt_token(token)
    owner = crud_user.get_user_by_username(db, owner_name)
    if not owner:
        INVALID_OWNER_ID
    return owner
