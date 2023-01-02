from .models import User
from app.ents.user import dependencies
from app.ents.user import crud

from .endpoints import router as endpoints_router
from .login import router as login_router
