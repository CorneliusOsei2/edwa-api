from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app.ents.user import models, schema, crud, dependencies
from app.ents.employee.schema import EmployeeCreate


from app.core.config import settings
from app.utilities import utils

router = APIRouter()


@router.get("/individual-clients", response_model=list[schema.UserRead])
def get_individual_clients(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    """
    Retrieve Individual Clients.
    """
    employees = crud.user.read_multi_with_role(
        db, role=schema.Role.individualClient.value, skip=skip, limit=limit
    )
    return employees


@router.get("/business-clients", response_model=list[schema.UserRead])
def get_business_clients(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    """
    Retrieve Business Clients.
    """
    business_clients = crud.user.read_multi_with_role(
        db, role=schema.Role.businessClient.value, skip=skip, limit=limit
    )
    return business_clients


@router.post("/client", response_model=schema.UserRead)
def create_user(
    *,
    db: Session = Depends(dependencies.get_db),
    user_in: schema.UserCreate,
    current_user: models.User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    """
    Create a Client.
    """
    user = crud.user.read_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        utils.send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schema.UserRead)
def update_user_me(
    *,
    db: Session = Depends(dependencies.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(dependencies.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schema.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schema.UserRead)
def get_current_user(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schema.UserRead)
def create_user_open(
    *,
    db: Session = Depends(dependencies.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
    role: schema.Role = Body(...),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.read_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schema.UserCreate(
        password=password, email=email, full_name=full_name, role=role.value
    )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schema.UserRead)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(dependencies.get_current_active_user),
    db: Session = Depends(dependencies.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.read(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schema.UserRead)
def update_user(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    user_in: schema.UserUpdate,
    current_user: models.User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.read(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
