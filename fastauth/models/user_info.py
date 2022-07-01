import imp
from sqlalchemy import String, Column, Integer
from fastauth.db.database import Base
from sqlalchemy.orm import relationship


class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    fullname = Column(String)
