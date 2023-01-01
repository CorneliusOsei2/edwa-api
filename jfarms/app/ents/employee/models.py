from sqlalchemy import Boolean, Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base

employees_sales = Table(
    "employees_sales",
    Base.metadata,
    Column("employee_id", ForeignKey("employees.id")),
    Column("sale_id", ForeignKey("sales.id")),
)


class Employee(Base):  # type: ignore
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    job_title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    location = Column(String, nullable=False)
    supervisor = Column(String, nullable=True)
    month_salary = Column(Integer, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    sales = relationship("Sale", secondary=employees_sales)
