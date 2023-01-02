from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app.ents.employee import crud, dependencies, models, schema
import app.ents.user as user
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/employees", response_model=list[schema.EmployeeRead])
def get_employees(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    _: user.models.User = Depends(user.dependencies.get_current_active_superuser),
) -> Any:
    """
    Retrieve Employees.
    """
    employees = crud.employee.read_multi(db, skip=skip, limit=limit)
    return employees


@router.post("/employees", response_model=schema.EmployeeRead)
def create_employee(
    *,
    db: Session = Depends(dependencies.get_db),
    employee_in: schema.EmployeeCreate,
    _: user.models.User = Depends(user.dependencies.get_current_active_board_member),
) -> Any:
    """
    Create an Employee.
    """
    employee = crud.employee.read_by_email(db, email=employee_in.email)
    if employee:
        raise HTTPException(
            status_code=400,
            detail="The employee with this username already exists in the system.",
        )

    employee = crud.employee.create(
        db, obj_in=schema.EmployeeCreate(**employee_in.dict())
    )
    if settings.EMAILS_ENABLED and employee_in.email:
        send_new_account_email(
            email_to=employee_in.email,
            username=employee_in.email,
            password=employee_in.password,
        )
    return employee


@router.put("/employees/{user_id}", response_model=schema.EmployeeRead)
def update_employee(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    user_in: schema.EmployeeUpdate,
    _: user.User = Depends(user.dependencies.get_current_active_board_member),
) -> Any:
    """
    Update Employee.
    """
    user = crud.employee.read(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.employee.update(db, db_obj=user, obj_in=user_in)
    return user
