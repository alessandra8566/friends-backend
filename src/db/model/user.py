from db import Base, Column, String, Integer, UUID, relationship, DateTime
from enum import Enum as PyEnum

class Role(PyEnum):
    ADMIN       = "admin"
    VIP1_USER   = "vip1_user"
    VIP2_USER   = "vip2_user"
    BASE_USER   = "user"

class User(Base):
    __tablename__ = 'user'
    
    id              = Column(UUID(as_uuid=True), primary_key=True)
    name            = Column(String, nullable=False)
    email           = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    role            = Column(String)
    refresh_token   = Column(String, unique=True)
    create_at       = Column(DateTime, unique=True, nullable=False)