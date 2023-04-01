from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.ents import user
from app.ents.employee import auth, crud, dependencies, models, schema

router = APIRouter(prefix="/employees")


@router.post("/login")
def login_employee(response: Response, token=Depends(auth.login_access_token)) -> Any:
    """
    Log Employee in.
    """
    # response.headers[
    #     "Authorization"
    # ] = f'{token.get("type")} {token.get("access_token")}'
    response.set_cookie(
        key ="access_token", value= token.get("access_token"), samesite=None)
    return token


@router.get("", response_model=list[schema.EmployeeRead])
def get_employees(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    # _: str = Depends(dependencies.get_current_employee),
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
    # _=Depends(get_current_employee),
) -> Any:
    """
    Create an Employee.
    """
    employee = crud.employee.read_by_email(db, email=employee_in.email)
    if employee:
        raise HTTPException(
            status_code=400,
            detail="The employee with this email already exists!.",
        )

    employee = crud.employee.create(db, employee_in=employee_in)
    return employee


@router.put("/{user_id}", response_model=schema.EmployeeRead)
def update_employee(
    *,
    db: Session = Depends(dependencies.get_db),
    employee_in: schema.EmployeeUpdate,
    employee: models.Employee = Depends(dependencies.get_current_employee),
) -> Any:
    """
    Update Employee.
    """
    employee = crud.employee.read(db, id=employee.id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="The employee with this employee name does not exist in the system",
        )
    employee = crud.employee.update(
        db, db_obj=employee, employee_in=employee_in)
    return user
