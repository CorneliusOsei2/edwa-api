from app.database.base_class import Base
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.orm import relationship


class EmployeeID(Base):  # type: ignore
    __tablename__ = "employee_ids"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    initials = Column(String, nullable=False)
    tag = Column(String, nullable=False)


class Sale(Base):  # type: ignore
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    balance = Column(Float, default=0.0)


employees_sales = Table(
    "employees_sales",
    Base.metadata,
    Column("employee_id", ForeignKey("employees.id")),
    Column("sale_id", ForeignKey("sales.id")),
)


class Employee(Base):  # type: ignore
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    first_name = Column(String, index=True, nullable=False)
    middle_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=False)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    contact = Column(String, unique=True, nullable=False)
    home_address = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    job_title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    work_address = Column(String, nullable=False)
    supervisor_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    monthly_salary = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    sales = relationship("Sale", secondary=employees_sales)
