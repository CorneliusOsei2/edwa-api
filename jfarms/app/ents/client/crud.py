from typing import Any

from app.base import crud_base
from app.core.security import get_password_hash, verify_password
from app.ents.client.models import Client
from app.ents.client.schema import ClientCreate, ClientUpdate
from sqlalchemy.orm import Session
from typing_extensions import override


class CRUDClient(crud_base.CRUDBase[Client, ClientCreate, ClientUpdate]):
    def read_by_email(self, db: Session, *, email: str) -> Client | None:
        return db.query(Client).filter(Client.email == email).first()

    def read_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Client]:
        return db.query(Client).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: ClientCreate) -> Client:
        db_obj = Client(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            username=obj_in.username,
            location=obj_in.location,
            is_active=obj_in.is_active,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Client, obj_in: ClientUpdate | dict[str, Any]
    ) -> Client:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Client | None:
        client = self.read_by_email(db, email=email)
        if not client:
            return None
        # type: ignore  Column--warning
        if not verify_password(password, client.hashed_password):
            return None
        return client

    def is_active(self, client: Client) -> bool:
        return client.is_active  # type: ignore  Column--warning

    def is_superclient(self, user: Client) -> bool:
        return client.is_superuser  # type: ignore  Column--warning


client = CRUDClient(Client)
