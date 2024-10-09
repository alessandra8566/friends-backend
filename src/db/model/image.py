from db import Base, Column, String, Integer, ForeignKey, UUID, relationship, DateTime, Boolean

class Image(Base):
    __tablename__ = 'image'
    
    id                = Column(UUID(as_uuid=True), primary_key=True)
    name              = Column(String, nullable=False)
    url               = Column(String, nullable=False)
    index             = Column(Integer, nullable=True)
    user_profile_id   = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'))
    avatar            = Column(Boolean, default=False)
    created_at        = Column(DateTime, nullable=False)
    updated_at        = Column(DateTime, nullable=False)
    
    user_profile      = relationship('Profile', back_populates='images')