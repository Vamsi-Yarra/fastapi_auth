from fastapi import APIRouter, Depends, HTTPException, Request
from fastauth.auth import auth
from fastauth.crud import crud_user
from fastauth.schemas import schemas_user
from sqlalchemy.orm import Session
from fastauth.dependencies import get_db
from datetime import timedelta
import time

user_router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 15


@user_router.post("/users/register", status_code=201, response_model=schemas_user.UserInfo, tags=['users'])
def register_user(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=409, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)


@user_router.post("/users/auth", response_model=schemas_user.Token, tags=['users'])
def auth_user(user: schemas_user.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(
            status_code=403, detail='Username or password is incorrect')
    else:
        is_password_correct = auth.check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(
                status_code=403, detail='Username or password is incorrect')
        else:
            access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = auth.encode_jwt_token(
                data={"sub": user.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "Bearer"}


@user_router.get("/users/current_user", tags=['Users'])
def get_current_user(token: str):
    return auth.decode_jwt_token(token)
