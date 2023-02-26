from datetime import datetime, timedelta
from typing import Any

from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str = ""


class Security:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self,
                            subject: str | Any, expires_delta: timedelta | None = None
                            ) -> str:
        """Creates an access token

        Args:
            subject (str | Any): Token payload, typically the entity id.
            expires_delta (timedelta | None, optional): Lifetime of token in minutes. Defaults to None.

        Returns:
            str: Encoded token string
        """

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            claims=to_encode, key=settings.SECRET_KEY, algorithm="HS256"
        )
        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Checks if `plain_password` is `hashed_password`.

        Args:
            plain_password (str): User input password.
            hashed_password (str): Hashed password with passlib

        Returns:
            bool: If the two passwords are same.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)


security = Security()
