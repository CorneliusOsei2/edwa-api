from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Form
from fastapi.encoders import jsonable_encoder
from app.ents.client.login import login_access_token
from app.ents.user.dependencies import get_db
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app.ents.client import crud, dependencies, models, schema
import app.ents.user as user
from app.core.config import settings
from app.utilities import utils

router = APIRouter()


@router.post("/login")
def login_client(username=Form(), password=Form(), db: Session = Depends(get_db), token=Depends(login_access_token)) -> Any:
    """
    Log Client in.
    """
    return token


@router.get("/clients", response_model=list[schema.ClientRead])
def get_clients(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    _: user.models.User = Depends(
        user.dependencies.get_current_active_superuser),
) -> Any:
    """
    Retrieve Clients.
    """
    clients = crud.client.read_multi(db, skip=skip, limit=limit)
    return clients


@router.post("/clients", response_model=schema.ClientRead)
def create_client(
    *,
    db: Session = Depends(dependencies.get_db),
    user_in: schema.ClientCreate,
    _: user.models.User = Depends(
        user.dependencies.get_current_active_superuser),
) -> Any:
    """
    Create an Client.
    """
    user = crud.client.read_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.client.create(db, obj_in=schema.ClientCreate(**user_in.dict()))
    if settings.EMAILS_ENABLED and user_in.email:
        utils.send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/clients/{user_id}", response_model=schema.ClientRead)
def update_client(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    user_in: schema.ClientUpdate,
    _: user.User = Depends(user.dependencies.get_current_active_superuser),
) -> Any:
    """
    Update Client.
    """
    user = crud.client.read(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.client.update(db, db_obj=user, obj_in=user_in)
    return user
