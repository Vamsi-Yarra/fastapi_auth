from telnetlib import SE
import bcrypt
from sqlalchemy.orm import Session
from fastauth.models import item
from ..schemas import schemas_item


def get_item_by_item_name(db: Session, item_name: str):
    # will remove this
    return db.query(item.Items).filter(item.Items.item_name == item_name).first()


def get_item_by_item_id(db: Session, item_id: str):
    # will remove this
    return db.query(item.Items).filter(item.Items.id == item_id).first()


def create_item(db: Session, new_item: schemas_item.ItemsCreate):

    db_item = item.Items(item_name=new_item.item_name,
                         item_type=new_item.item_type, owner_id=new_item.owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Item update and delete and owner conditions

def update_item(db: Session, item_id: int, update_item: schemas_item.ItemsUpdate):
    db_item = get_item_by_item_id(db, item_id)
    db_item.item_name = update_item.item_name
    db_item.item_type = update_item.item_type

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = get_item_by_item_id(db, item_id)

    db.delete(db_item)
    db.commit()
    return db_item
