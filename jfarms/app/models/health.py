from sqlalchemy import Boolean, Column, Integer
from app.database.base_class import Base


class Health(Base):  # type: ignore
    __tablename__ = "health"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Integer, index=True, nullable=False)
    immunized = Column(Boolean, nullable=False)
    poisoned = Column(Boolean, nullable=False)
