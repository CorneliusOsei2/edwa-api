from app.database.base_class import Base
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.orm import relationship

clients_sales = Table(
    "clients_sales",
    Base.metadata,
    Column("client_id", ForeignKey("clients.id")),
    Column("sale_id", ForeignKey("sales.id")),
)


class Client(Base):  # type: ignore
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    location = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    sales = relationship("Sale", secondary=clients_sales)
