from datetime import datetime

from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: str = ""
    last_name: str
    contact: str = ""
    home_address: str = ""
    work_address: str = ""
    job_title: str = ""
    department: str = ""
    monthly_salary: float = 0.0
    supervisor_id: int | None = None
    is_active: bool = True
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()


class EmployeeCreate(EmployeeBase):
    password: str


class EmployeeUpdate(EmployeeBase):
    ...


class EmployeeInDBBase(EmployeeBase):
    id: int | None = None
    username: str = ""
    full_name: str = ""

    class Config:
        orm_mode = True


class EmployeeInDB(EmployeeInDBBase):
    password: str


class EmployeeRead(EmployeeInDBBase):
    ...
