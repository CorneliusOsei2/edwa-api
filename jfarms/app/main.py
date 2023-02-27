from app.core.config import Settings
from app.core.config import settings
from app.ents.api import api_router
from app.prestart import initial_data
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException


@AuthJWT.load_config
def get_config():
    return Settings()


def create_app():
    """Creates an instance of FastAPI application."""
    return FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
    )


def enable_cors(app):
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin)
                           for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


app = create_app()
enable_cors(app)
app.include_router(api_router, prefix=settings.API_STR)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


initial_data.main()
