from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel


class ImageBase(BaseModel):
    name: str
    url: str
    index: int
    avatar: bool
    user_profile_id: UUID
    
    class Config:
        orm_mode = True

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True

