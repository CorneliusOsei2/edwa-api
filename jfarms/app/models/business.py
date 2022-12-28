from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(Integer, nullable=False)
    trade_in = Column(String, nullable=False)
    worth = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="businesses")
    is_active = Column(Boolean(), default=True)
