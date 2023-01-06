from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class Role(Enum):
    board = "Board"
    manager = "Manager"
    employee = "Employee"
    businessClient = "Business Client"
    individualClient = "Individual Client"
    investor = "Investor"


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = True
    is_superuser: bool = False
    full_name: str | None
    username: str = ""
    role: str = Role.individualClient.value
    start_date: datetime = datetime.today()
    end_date: datetime = datetime.today()


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: EmailStr
    password: str

# Properties to receive via API on update


class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserRead(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
