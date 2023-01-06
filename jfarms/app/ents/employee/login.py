from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import config, security
from app.ents.employee import crud, dependencies, models, schema
from app.utilities import utils

router = APIRouter()


@router.post("/employees/login/access-token", response_model=security.Token)
def login_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    employee = crud.employee.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not employee:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.employee.is_active(employee):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {
        "access_token": security.create_access_token(
            employee.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/employees/login/test-token", response_model=schema.EmployeeRead)
def test_token(
    current_employee: models.Employee = Depends(dependencies.get_current_employee),
) -> Any:
    """
    Test access token
    """
    return current_employee


# @router.post("/password-recovery/{email}", response_model=schema.Msg)
# def recover_password(email: str, db: Session = Depends(dependencies.get_db)) -> Any:
#     """
#     Password Recovery
#     """
#     employee = crud.employee.read_by_email(db, email=email)

#     if not employee:
#         raise HTTPException(
#             status_code=404,
#             detail="The employee with this username does not exist in the system.",
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
#     email =utils.verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     employee = crud.employee.read_by_email(db, email=email)
#     if not employee:
#         raise HTTPException(
#             status_code=404,
#             detail="The employee with this username does not exist in the system.",
#         )
#     elif not crud.employee.is_active(employee):
#         raise HTTPException(status_code=400, detail="Inactive employee")
#     hashed_password = get_password_hash(new_password)
#     employee.hashed_password = hashed_password  # type: ignore  Column--warning
#     db.add(employee)
#     db.commit()
#     return {"schemas.Msg": "Password updated successfully"}
