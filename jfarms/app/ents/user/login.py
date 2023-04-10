from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import config
from app.core.security import Token, security
from app.ents.user import crud, dependencies, models, schema
from app.utilities import msg, utils

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "Bearer",
    }


@router.post("/login/test-token", response_model=schema.UserRead)
def test_token(
    current_user: models.User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=msg.Msg)
def recover_password(email: str, db: Session = Depends(dependencies.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.read_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = utils.generate_password_reset_token(email=email)
    utils.send_reset_password_email(
        # type: ignore  Column--warning
        email_to=user.email,
        email=email,
        token=password_reset_token,
    )
    return {"schemas.Msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=msg.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(dependencies.get_db),
) -> Any:
    """
    Reset password
    """
    email = utils.verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.read_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = security.get_password_hash(new_password)
    user.hashed_password = hashed_password  # type: ignore  Column--warning
    db.add(user)
    db.commit()
    return {"schemas.Msg": "Password updated successfully"}
