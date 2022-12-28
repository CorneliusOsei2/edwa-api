from sqlalchemy.orm import Session
from .. import crud, schemas

from app.core.config import settings
from app.schemas.user import Role  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.read_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            full_name=settings.FIRST_SUPERUSER_FULL_NAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            role=Role.board.value,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
