from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.prestart import prestart
from app.core.config import settings
from app.database.init_db import init_db
from app.database.session import SessionLocal

from app.ents.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

prestart.main()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_STR)
