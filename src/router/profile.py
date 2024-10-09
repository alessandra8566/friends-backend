from uuid import UUID
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from router.collection.image import UserImagesCollection
from schema.user import User
from . import validate_token, get_db
import schema, crud

router = APIRouter()

@router.get("", response_model=schema.Profile)
def get_my_profile(db: Session = Depends(get_db), user: User = Depends(validate_token)):
    users = crud.get_profile_by_id(db, user.id)
    return users

@router.get("/view/{profile_id}", response_model=schema.UserProfile)
def get_profile(profile_id: UUID, db: Session = Depends(get_db), _: None = Depends(validate_token)):
    user_profile = crud.get_user_profile_by_id(db, profile_id)
    return user_profile

@router.patch("/{profile_id}", response_model=schema.Profile)
def path_user_profile(profile_id: UUID, profile_info: schema.ProfilePatch, db: Session = Depends(get_db), _: None = Depends(validate_token)):
    user_profile = crud.patch_profile(db, profile_id, profile_info)
    return user_profile

@router.post("/{profile_id}/image", response_model=schema.Image)
def post_images(profile_id: UUID, index: str = Form(...), avatar: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db), _: None = Depends(validate_token)):
    _collect = UserImagesCollection(db)
    db_images = _collect.upload_image(profile_id, index, avatar, file)
    return db_images

@router.delete("/{profile_id}/image/{image_id}")
def delete_image(profile_id: UUID, image_id: UUID, db: Session = Depends(get_db), _: None = Depends(validate_token)):
    _collect = UserImagesCollection(db)
    _collect.delete_image(profile_id, image_id)
    return "success"

@router.get("/avatars", response_model=List[schema.Profile])
def get_profiles_with_avatar(db: Session = Depends(get_db), _: None = Depends(validate_token)):
    profiles = crud.get_profile_list_with_avatar(db)
    return profiles