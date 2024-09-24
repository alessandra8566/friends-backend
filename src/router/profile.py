from uuid import UUID
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from router.collection.image import UserImagesCollection
from schema.user import User
from . import validate_token, get_db
import schema, crud

router = APIRouter()

@router.get("", response_model=schema.UserProfile)
def get_my_profile(db: Session = Depends(get_db), user: User = Depends(validate_token)):
    users = crud.get_profile_by_user_id(db, user.id)
    return users

@router.patch("/{profile_id}", response_model=schema.UserProfile)
def path_user_profile(profile_id: UUID, profile_info: schema.UserProfilePatch, db: Session = Depends(get_db), _: None = Depends(validate_token)):
    user_profile = crud.patch_user_profile(db, profile_id, profile_info)
    return user_profile
  
@router.post("/{profile_id}/image", response_model=schema.Image)
def post_images(profile_id: UUID, index: str = Form(...), avatar: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db), _: None = Depends(validate_token)):
    _collect = UserImagesCollection(db)
    db_images = _collect.upload_image(profile_id, index, avatar, file)
    return db_images