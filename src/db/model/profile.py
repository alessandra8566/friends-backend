from db import Base, Column, String, UUID, relationship, DateTime, ForeignKey

class UserProfile(Base):
    __tablename__ = 'user_profile'
    
    id              = Column(UUID(as_uuid=True), primary_key=True)
    user_id         = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'))
    description     = Column(String, nullable=True)
    create_at       = Column(DateTime, unique=True, nullable=False)
    
    # 一對多關係
    images = relationship('Image', back_populates='user_profile')