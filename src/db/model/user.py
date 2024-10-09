from db import Base, Column, String, UUID, DateTime, Enum as SQLEnum
from enum import Enum

class Role(str, Enum):
    ADMIN       = "admin"
    VIP1_USER   = "vip1_user"
    VIP2_USER   = "vip2_user"
    BASE_USER   = "user"
    
class Gender(str, Enum):
    MALE   = "male"
    FEMALE = "female"

class User(Base):
    __tablename__ = 'user'
    
    id              = Column(UUID(as_uuid=True), primary_key=True)
    email           = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    birthday        = Column(String, nullable=False)
    gender          = Column(SQLEnum(Gender), nullable=False)
    role            = Column(SQLEnum(Role), nullable=False)
    refresh_token   = Column(String, unique=True)
    created_at      = Column(DateTime, unique=True, nullable=False)
    updated_at      = Column(DateTime, unique=True, nullable=False)