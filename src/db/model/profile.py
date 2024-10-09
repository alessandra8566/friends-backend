from db import Base, Column, String, UUID, relationship, DateTime, ForeignKey, Integer, Enum as SQLEnum
from enum import Enum

class Frequency(str, Enum):
    ALWAYS      = "always"
    SOMETIMES   = "sometimes"
    NEVER       = "never"
    
class Profile(Base):
    __tablename__ = 'user_profile'
    
    id              = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    name            = Column(String, nullable=False)
    introduce       = Column(String, nullable=True)
    like_style      = Column(String, nullable=True)
    constellation   = Column(String, nullable=True)
    location        = Column(String, nullable=True)
    weight          = Column(Integer, nullable=True)
    height          = Column(Integer, nullable=True)
    job             = Column(String, nullable=True)
    education       = Column(String, nullable=True)
    hobby           = Column(String, nullable=True)
    smoke           = Column(SQLEnum(Frequency), nullable=True)
    drink           = Column(SQLEnum(Frequency), nullable=True)
    languages       = Column(String, nullable=True)
    created_at      = Column(DateTime, unique=True, nullable=False)
    updated_at      = Column(DateTime, nullable=False)
    
    # 一對多關係
    images = relationship('Image', back_populates='user_profile')