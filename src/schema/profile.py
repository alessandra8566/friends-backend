from typing import List
from uuid import UUID
from pydantic import BaseModel

from schema.image import Image


class UserProfileBase(BaseModel):
    description: str = ""
    class Config:
        orm_mode = True

class UserProfilePatch(UserProfileBase):
	pass

class UserProfileCreate(UserProfileBase):
    user_id: UUID
    pass

class UserProfile(UserProfileBase):
    id: UUID
    user_id: UUID
    
    images: List[Image] = []
    class Config:
        orm_mode = True