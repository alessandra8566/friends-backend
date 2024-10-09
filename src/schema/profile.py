from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from db.model.profile import Frequency
from db.model.user import Gender
from schema.image import Image


class ProfileBase(BaseModel):
    name: str = ""
    introduce: Optional[str] = None
    like_style: Optional[str] = None
    constellation: Optional[str] = None
    location: Optional[str] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    job: Optional[str] = None
    education: Optional[str] = None
    hobby: Optional[str] = None
    smoke: Optional[Frequency] = None
    drink: Optional[Frequency] = None
    languages: Optional[str] = None
    class Config:
        orm_mode = True

class ProfilePatch(ProfileBase):
    pass
class ProfileCreate(ProfileBase):
    id: UUID

class Profile(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime 
    
    images: List[Image] = []
    class Config:
        orm_mode = True
        
class UserProfile(Profile):
    birthday: str
    gender: Gender