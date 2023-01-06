from datetime import datetime

from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    email: EmailStr
    full_name: str
    username: str
    job_title: str = ""
    department: str = ""
    location: str = ""
    monthly_salary: float = 0.0
    supervisor_id: int | None = None
    is_active: bool = True
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()


class ClientCreate(ClientBase):
    password: str


class ClientUpdate(ClientBase):
    ...


class ClientRead(ClientBase):
    ...
