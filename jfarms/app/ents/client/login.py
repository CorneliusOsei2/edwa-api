from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import config, security
from app.ents.client import crud, dependencies, models, schema
from app.utilities import utils

router = APIRouter()


@router.post("/clients/login/access-token", response_model=security.Token)
def login_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    client = crud.client.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not client:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.client.is_active(client):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {
        "access_token": security.create_access_token(
            client.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/clients/login/test-token", response_model=schema.ClientRead)
def test_token(
    current_client: models.Client = Depends(dependencies.get_current_client),
) -> Any:
    """
    Test access token
    """
    return current_client


# @router.post("/password-recovery/{email}", response_model=schema.Msg)
# def recover_password(email: str, db: Session = Depends(dependencies.get_db)) -> Any:
#     """
#     Password Recovery
#     """
#     client = crud.client.read_by_email(db, email=email)

#     if not client:
#         raise HTTPException(
#             status_code=404,
#             detail="The client with this username does not exist in the system.",
#         )
#     password_reset_token = utils.generate_password_reset_token(email=email)
#     utils.send_reset_password_email(
#         email_to=user.email, email=email, token=password_reset_token  # type: ignore  Column--warning
#     )
#     return {"schemas.Msg": "Password recovery email sent"}


# @router.post("/reset-password/", response_model=schemas.Msg)
# def reset_password(
#     token: str = Body(...),
#     new_password: str = Body(...),
#     db: Session = Depends(dependencies.get_db),
# ) -> Any:
#     """
#     Reset password
#     """
#     email = utils.verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     client = crud.client.read_by_email(db, email=email)
#     if not client:
#         raise HTTPException(
#             status_code=404,
#             detail="The client with this username does not exist in the system.",
#         )
#     elif not crud.client.is_active(client):
#         raise HTTPException(status_code=400, detail="Inactive client")
#     hashed_password = get_password_hash(new_password)
#     client.hashed_password = hashed_password  # type: ignore  Column--warning
#     db.add(client)
#     db.commit()
#     return {"schemas.Msg": "Password updated successfully"}
