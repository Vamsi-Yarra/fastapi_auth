import datetime
import jwt
import os
from requests import request
from sqlalchemy.orm import Session
import bcrypt
from fastapi import HTTPException, status
from dotenv import load_dotenv
from fastauth.models import user_info
from fastauth.crud import crud_user
from ..schemas import schemas_user

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


def check_username_password(db: Session, user: schemas_user.UserAuthenticate):
    db_user_info: user_info.UserInfo = crud_user.get_user_by_username(
        db, user.username)
    db_password = db_user_info.password.encode('utf-8')
    request_password = user.password.encode('utf-8')
    return bcrypt.checkpw(request_password, db_password)


def encode_jwt_token(*, data: dict, expires_delta: datetime.timedelta = None):
    encode_date = data.copy()
    if expires_delta:
        expires = datetime.datetime.utcnow() + expires_delta
    else:
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    encode_date.update({"exp": expires})

    encode_jwt = jwt.encode(encode_date, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encode_jwt


def decode_jwt_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except:
        return "Token Error"
