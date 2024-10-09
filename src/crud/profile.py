from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session, joinedload
from db.model import Profile, Image, User
from schema import ProfileCreate, ProfilePatch, ImageCreate


def get_profile_by_id(db: Session, id: UUID):
    try:
        db_user_profile = db.query(Profile).filter(Profile.id == id).first()
        return db_user_profile
    except Exception as e:
        raise e
def get_user_profile_by_id(db: Session, id: UUID):
    try:
        db_user_profile = db.query(Profile).filter(Profile.id == id).first()
        db_user = db.query(User).filter(User.id == id).first()
        db_user_profile.gender = db_user.gender
        db_user_profile.birthday = db_user.birthday
        return db_user_profile
    except Exception as e:
        raise e
    
def get_profile_list_with_avatar(db: Session, limit: int = 30):
    try:
        profiles_with_avatar_images = db.query(Profile).join(Profile.images).filter(Image.avatar == True).options(joinedload(Profile.images)).all()
        return profiles_with_avatar_images
    except Exception as e:
        raise e

def post_profile(db: Session, user: ProfileCreate):
    try:
        db_user_profile = Profile(
            id=user.id,
            name=user.name,
            introduce=user.introduce,
            like_style=user.like_style,
            constellation=user.constellation,
            location=user.location,
            weight=user.weight,
            height=user.height,
            job=user.job,
            education=user.education,
            hobby=user.hobby,
            smoke=user.smoke,
            drink=user.drink,
            languages=user.languages,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(db_user_profile)
        db.commit()
        db.refresh(db_user_profile)
        
        return db_user_profile
    except Exception as e:
        raise e

def patch_profile(db: Session, id: UUID, profile: ProfilePatch):
    try:
        db_user_profile = db.query(Profile).filter(Profile.id == id).first()
        if db_user_profile:
            for key, value in profile.model_dump().items():
                setattr(db_user_profile, key, value)
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
                created_at=datetime.now(),
                updated_at=datetime.now()
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
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return db_image
    except Exception as e:
        raise e