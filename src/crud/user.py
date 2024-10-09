# user
from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from schema.image import Image
from schema.user import UserCreate
from db.model.user import User


def get_users(db: Session, limit: int = 10):
    try:
        return db.query(User).order_by(User.created_at.desc()).limit(limit).all()
    except Exception as e:
        raise e

def get_user(db: Session, user_id: int):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        raise e

def get_users_by_ids(db: Session, user_ids: List[UUID] = [], target_images: List[Image] = []):
    try:
        db_users = db.query(User).filter(User.id.in_(user_ids)).all()
        for user in db_users:
            target_image_ids = [image.id for image in target_images]
            user.images = list(filter(lambda image: image.id in target_image_ids, user.images))
            
        return db_users
    except Exception as e:
        raise e

def get_user_by_email(db: Session, email: str):
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        raise e

def post_user(db: Session, user: UserCreate):
    try:
        db_user = User(
            id=uuid4(),
            email=user.email,
            birthday=user.birthday,
            gender=user.gender,
            role=user.role,
            hashed_password=user.password,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except Exception as e:
        raise e