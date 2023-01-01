from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey

from app.database.base_class import Base


class Animal(Base):  # type: ignore
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, index=True, nullable=False)
    kind = Column(String, index=True, nullable=False)
    gender = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_alive = Column(Boolean(), default=True)
    health = Column(Integer, ForeignKey("health.id"))
    issues = Column(Integer, ForeignKey("issues.id"))
    notes = Column(String, nullable=True)
