from typing import Any

from app.core.config import settings
from app.ents import user
from app.ents.employee import crud, dependencies, models, schema
from app.ents.employee.login import login_access_token
from app.ents.user.dependencies import get_db
from app.utilities import utils
from fastapi import APIRouter, Body, Depends, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

router = APIRouter(prefix="/employees")


@router.post("/login")
def login_employee(username=Form(), password=Form(), db: Session = Depends(get_db), token=Depends(login_access_token)) -> Any:
    """
    Log Employee in.
    """
    return token


@router.get("", response_model=list[schema.EmployeeRead])
def get_employees(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    _: user.models.User = Depends(
        user.dependencies.get_current_active_user),
) -> Any:
    """
    Retrieve Employees.
    """
    employees = crud.employee.read_multi(db, skip=skip, limit=limit)
    return employees


@router.post("/", response_model=schema.EmployeeRead)
def create_employee(
    *,
    db: Session = Depends(dependencies.get_db),
    employee_in: schema.EmployeeCreate,
    _: user.models.User = Depends(
        user.dependencies.get_current_active_board_member),
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
        utils.send_new_account_email(
            email_to=employee_in.email,
            username=employee_in.email,
            password=employee_in.password,
        )
    return employee


@router.put("/{user_id}", response_model=schema.EmployeeRead)
def update_employee(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    user_in: schema.EmployeeUpdate,
    _: user.models.User = Depends(
        user.dependencies.get_current_active_board_member),
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
