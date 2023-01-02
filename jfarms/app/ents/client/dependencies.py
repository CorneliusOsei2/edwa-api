from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ents.client import crud, models
from app.core.config import settings
from app.core.security import TokenPayload
from app.database.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}/clients/login/access-token"
)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_client(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.Client:
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=["HS256"])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    client = crud.client.read(db, id=token_data.sub)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


def get_current_active_user(
    current_user: models.Client = Depends(get_current_client),
) -> models.Client:
    if not crud.client.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
