from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class Role(str, Enum):
    ADMIN       = "admin"
    VIP1_USER   = "vip1_user"
    VIP2_USER   = "vip2_user"
    BASE_USER   = "user"

class UserBase(BaseModel):
    name: str
    email: str
    role: Role = "user"
    
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str
    class Config:
        orm_mode = True

class User(UserBase):
    id: UUID
    create_at: datetime
    
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
    hashed_password: Optional[str] = None
    role: Optional[Role] = None