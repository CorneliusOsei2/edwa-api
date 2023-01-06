# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base_class import Base  # noqa
from app.ents.animal.models import Animal, Health
from app.ents.employee.models import Employee  # noqa
from app.ents.user.models import User  # noqa
