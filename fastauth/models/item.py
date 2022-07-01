from sqlalchemy import ForeignKey, String, Column, Integer
from fastauth.db.database import Base
from sqlalchemy.orm import relationship


class Items(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, unique=True)
    item_type = Column(String)
    owner_id = Column(Integer, ForeignKey("user_info.id"))
