from typing import Any

from app.base import crud_base
from app.core.security import get_password_hash, verify_password
from app.ents.user import crud, models, schema
from sqlalchemy.orm import Session


class CRUDUser(crud_base.CRUDBase[models.User, schema.UserCreate, schema.UserUpdate]):
    def read_by_email(self, db: Session, *, email: str) -> models.User | None:
        return db.query(models.User).filter(models.User.email == email).first()

    def read_multi_with_role(
        self, db: Session, *, role: str, skip: int = 0, limit: int = 100
    ) -> list[models.User]:
        return (
            db.query(models.User)
            .filter(models.User.role == role)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: schema.UserCreate) -> models.User:
        db_obj = models.User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            role=obj_in.role,
            is_superuser=obj_in.is_superuser,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: models.User,
        obj_in: schema.UserUpdate | dict[str, Any]
    ) -> models.User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> models.User | None:
        user = self.read_by_email(db, email=email)
        if not user:
            return None
        # type: ignore  Column--warning
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_role(self, user: models.User) -> str:
        return user.role  # type: ignore  Column--warning

    def is_active(self, user: models.User) -> bool:
        return user.is_active  # type: ignore  Column--warning

    def is_superuser(self, user: models.User) -> bool:
        return user.is_superuser  # type: ignore  Column--warning


user = CRUDUser(models.User)
