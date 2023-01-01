from sqlalchemy import Boolean, Column, Integer, String, DateTime
from app.database.base_class import Base


class Issue(Base):  # type: ignore
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
