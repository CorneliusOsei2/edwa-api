from sqlalchemy import Boolean, Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base

clients_sales = Table(
    "clients_sales",
    Base.metadata,
    Column("client_id", ForeignKey("clients.id")),
    Column("sale_id", ForeignKey("sales.id")),
)


class Client(Base):  # type: ignore
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    company_name = Column(String, nullable=False)
    is_business = Column(Boolean, default=False)
    location = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=True)
    sales = relationship("Sale", secondary=clients_sales)
