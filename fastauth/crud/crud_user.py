from telnetlib import SE
import bcrypt
from sqlalchemy.orm import Session
from fastauth.models import user_info
from ..schemas import schemas_user


def get_user_by_username(db: Session, username: str):
    return db.query(user_info.UserInfo).filter(user_info.UserInfo.username == username).first()


def create_user(db: Session, user: schemas_user.UserCreate):
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    db_user = user_info.UserInfo(username=user.username,
                                 fullname=user.fullname, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
