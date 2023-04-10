# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base_class import Base
# from app.ents.animal.models import Animal, Health
from app.ents.employee.models import Employee
from app.ents.user.models import User
