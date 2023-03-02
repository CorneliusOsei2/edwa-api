from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from app.core.config import settings
from app.ents.api import api_router
from app.prestart import initial_data


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


@app.get("/")
def greet(response: Response, authorization=Header()):
    response.headers["Authorization"] = authorization
    return "Hi"


initial_data.main()
