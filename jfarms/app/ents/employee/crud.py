from typing import Any

from app.base import crud_base
from app.core import security
from app.ents.employee import models, schema
from sqlalchemy.orm import Session


class CRUDEmployee(
    crud_base.CRUDBase[models.Employee,
                       schema.EmployeeCreate, schema.EmployeeUpdate]
):
    def read_by_email(self, db: Session, *, email: str) -> models.Employee | None:
        return db.query(models.Employee).filter(models.Employee.email == email).first()

    def read_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[models.Employee]:
        return db.query(models.Employee).offset(skip).limit(limit).all()

    def get_full_name(self, obj_in: schema.EmployeeCreate) -> str:
        return f"{obj_in.first_name} {obj_in.middle_name} {obj_in.last_name}"

    def _get_username(self, db: Session, obj_in: schema.EmployeeCreate) -> str:
        last_employee = (
            db.query(models.Employee).order_by(
                models.Employee.id.desc()).first()
        )
        return f"{obj_in.first_name[0]}{obj_in.last_name[0]}{str(last_employee.id if last_employee else 1)}"

    def create(self, db: Session, *, obj_in: schema.EmployeeCreate) -> models.Employee:
        hashed_password = security.get_password_hash(obj_in.password)

        obj = obj_in.dict(
            exclude={"password"},
            include={
                "full_name": self.get_full_name(obj_in),
                "username": self._get_username(db, obj_in),
                "hashed_password": hashed_password,
            },
        )

        db_obj = models.Employee(**obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: models.Employee,
        obj_in: schema.EmployeeUpdate | dict[str, Any],
    ) -> models.Employee:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = security.get_password_hash(
                update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> models.Employee | None:
        employee = self.read_by_email(db, email=email)
        if not employee:
            return None

        if not security.verify_password(password, employee.hashed_password):
            return None
        return employee

    def is_active(self, employee: models.Employee) -> bool:
        return bool(employee.is_active)

    def is_superemployee(self, user: models.Employee) -> bool:
        return employee.is_superuser


employee = CRUDEmployee(models.Employee)
