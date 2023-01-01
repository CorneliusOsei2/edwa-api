from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float
from app.database.base_class import Base


class Sale(Base):  # type: ignore
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    balance = Column(Float, default=0.0)
