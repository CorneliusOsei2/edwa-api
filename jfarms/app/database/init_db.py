from sqlalchemy.orm import Session

import app.ents.user as user
from app.core.config import settings
from app.ents.user.schema import Role, UserCreate

# make sure all SQL Alchemy models are imported (app.database.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # * If creating without Alembic
    # Base.metadata.create_all(bind=engine)

    superuser = user.crud.user.read_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not superuser:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            full_name=settings.FIRST_SUPERUSER_FULL_NAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            role=Role.board.value,
        )
        superuser = user.crud.user.create(db, obj_in=user_in)  # noqa: F841
