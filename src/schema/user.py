from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from db.model.user import Gender, Role

class UserBase(BaseModel):
    email: str
    birthday: str
    gender: Gender = Gender.MALE
    role: Role = Role.BASE_USER
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    name: str
    password: str
    class Config:
        orm_mode = True

class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    
class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    name: Optional[str] = None
    birthday: Optional[str] = None
    gender: Optional[Gender] = None
    hashed_password: Optional[str] = None
    role: Optional[Role] = None