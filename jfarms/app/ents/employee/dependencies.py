from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.ents.user.dependencies import get_db
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ents.employee import schema, crud, models
from app.core import config, security
from app.database.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_STR}/employees/login/access-token"
)


def get_current_employee(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.Employee:
    try:
        payload = jwt.decode(
            token=token, key=config.settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = security.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    employee = crud.employee.read(db, id=token_data.sub)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def get_current_active_employee(
    current_employee: models.Employee = Depends(get_current_employee),
) -> models.Employee:
    if not crud.employee.is_active(current_employee):
        raise HTTPException(status_code=400, detail="Inactive employee")
    return current_employee
