from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from schema import ImageCreate
from db.model.image import Image

    
def get_images(db: Session, limit: int = 30):
    try:
        return db.query(Image).order_by(Image.create_at.desc()).limit(limit).all()
    except Exception as e:
        raise e
    
def get_image(db: Session, image_id: int):
    try:
        return db.query(Image).filter(Image.id == image_id).first()
    except Exception as e:
        raise e

def get_images_by_ids(db: Session, image_ids: List[UUID]):
    try:
        return db.query(Image).filter(Image.id.in_(image_ids)).all()
    except Exception as e:
        raise e
def get_images_by_user_id(db: Session, user_id: int):
    try:
        return db.query(Image).filter(Image.user_id == user_id).all()
    except Exception as e:
        raise e
