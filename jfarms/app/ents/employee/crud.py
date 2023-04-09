from typing import Any

from sqlalchemy.orm import Session

from app.base import crud_base
from app.core.security import security
from app.ents.employee import models, schema


class CRUDEmployee(
    crud_base.CRUDBase[models.Employee, schema.EmployeeCreate, schema.EmployeeUpdate]
):
    def read_by_email(self, db: Session, *, email: str) -> models.Employee | None:
        return db.query(models.Employee).filter(models.Employee.email == email).first()

    def read_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[models.Employee]:
        return db.query(models.Employee).offset(skip).limit(limit).all()

    def get_full_name(self, employee_in: schema.EmployeeCreate) -> str:
        return f"{employee_in.first_name} {employee_in.middle_name} {employee_in.last_name}"

    def create(
        self, db: Session, *, employee_in: schema.EmployeeCreate
    ) -> models.Employee:
        employee_in.password = security.get_password_hash(employee_in.password)
        employee = models.Employee(
            **(employee_in.dict()),
            full_name=self.get_full_name(employee_in),
        )

        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    def update(
        self,
        db: Session,
        *,
        db_obj: models.Employee,
        employee_in: schema.EmployeeUpdate | dict[str, Any],
    ) -> models.Employee:
        if isinstance(employee_in, dict):
            update_data = employee_in
        else:
            update_data = employee_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = security.get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> models.Employee | None:
        employee = self.read_by_email(db, email=email)
        if not employee:
            return None

        if not security.verify_password(password, str(employee.password)):
            return None
        return employee

    def is_active(self, employee: models.Employee) -> bool:
        return bool(employee.is_active)

    def is_superemployee(self, user: models.Employee) -> bool:
        ...


employee = CRUDEmployee(models.Employee)
