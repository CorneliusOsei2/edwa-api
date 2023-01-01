from typing import Any
from typing_extensions import override

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import Role, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def read_by_email(self, db: Session, *, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def read_multi_with_role(
        self, db: Session, *, role: str, skip: int = 0, limit: int = 100
    ) -> list[User]:
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

    @override
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            role=obj_in.role,
            is_superuser=obj_in.is_superuser,
            superior=obj_in.superior,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @override
    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate | dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        user = self.read_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):  # type: ignore  Column--warning
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active  # type: ignore  Column--warning

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser  # type: ignore  Column--warning


user = CRUDUser(User)
