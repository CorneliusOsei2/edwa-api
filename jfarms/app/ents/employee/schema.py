from pydantic import BaseModel, EmailStr


class Employee(BaseModel):
    email: EmailStr
    full_name: str
    password: str
