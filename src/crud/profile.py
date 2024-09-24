from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session, joinedload
from db.model import UserProfile, Image
from schema import UserProfileCreate, UserProfilePatch, ImageCreate


def get_profile_by_user_id(db: Session, user_id: UUID):
    try:
        db_user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        return db_user_profile
    except Exception as e:
        raise e
    
def get_profile_by_id(db: Session, profile_id: UUID):
    try:
        db_user_profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
        return db_user_profile
    except Exception as e:
        raise e
    
def get_profile_list_with_avatar(db: Session, limit: int = 30):
    try:
        profiles_with_avatar_images = db.query(UserProfile).join(UserProfile.images).filter(Image.avatar == True).options(joinedload(UserProfile.images)).all()
        return profiles_with_avatar_images
    except Exception as e:
        raise e

def post_user_profile(db: Session, user: UserProfileCreate):
    try:
        db_user_profile = UserProfile(
            id=uuid4(),
            description=user.description,
            user_id=user.user_id,
            name=user.name,
            create_at=datetime.now()
        )
        
        db.add(db_user_profile)
        db.commit()
        db.refresh(db_user_profile)
        
        return db_user_profile
    except Exception as e:
        raise e

def patch_user_profile(db: Session, profile_id: UUID, profile: UserProfilePatch):
    try:
        db_user_profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
        if db_user_profile:
            db_user_profile.description = profile.description
            db.commit()
            db.refresh(db_user_profile)
            return db_user_profile
        else:
            return None
    except Exception as e:
        raise e

def post_profile_images(db: Session, image_list: List[ImageCreate]):
    try:
        db_images = [
            Image(
                id=uuid4(),
                name=image.name,
                url=image.url,
                index=image.index,
                avatar=image.avatar,
                user_id=image.profile_user_id,
                create_at=datetime.now()
            ) for image in image_list
        ]
        
        db.add_all(db_images)
        db.commit()
        
        for db_image in db_images:
            db.refresh(db_image)
        
        return db_images
    except Exception as e:
        raise e

def post_profile_image(db: Session, image: ImageCreate):
    try:
        db_image = Image(
            id=uuid4(),
            name=image.name,
            url=image.url,
            index=image.index,
            avatar=image.avatar,
            user_profile_id=image.user_profile_id,
            create_at=datetime.now()
        )
        
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return db_image
    except Exception as e:
        raise e