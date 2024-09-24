
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from router import get_db, validate_token
from router.collection.image import UserImagesCollection
import schema, crud


router = APIRouter()

@router.get("", response_model=List[schema.Image])
def read_images(limit: int = 100, db: Session = Depends(get_db), _: None = Depends(validate_token)):
    images = crud.get_images(db, limit=limit)
    return images

@router.post("/{user_profile_id}", response_model=List[schema.Image])
def post_images(user_profile_id: UUID, files: List[UploadFile] = File(...), db: Session = Depends(get_db), _: None = Depends(validate_token)):
    _collect = UserImagesCollection(db)
    db_images = _collect.upload_images(db, user_profile_id, files)
    return db_images
