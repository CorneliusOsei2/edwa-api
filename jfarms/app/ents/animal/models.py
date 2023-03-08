from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.database.base_class import Base


class Health(Base):  # type: ignore
    __tablename__ = "health"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Integer, index=True, nullable=False)
    immunized = Column(Boolean, nullable=False)
    poisoned = Column(Boolean, nullable=False)


class Issue(Base):  # type: ignore
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)


class Animal(Base):  # type: ignore
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, index=True, nullable=False)
    kind = Column(String, index=True, nullable=False)
    gender = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_alive = Column(Boolean(), default=True)
    health = Column(Integer, ForeignKey("health.id"), cascade="delete")
    issues = Column(Integer, ForeignKey("issues.id"), cascade="delete")
    notes = Column(String, nullable=True)
