from fastapi import APIRouter

from app.ents import animal, client, employee, user

api_router = APIRouter()

api_router.include_router(user.login_router, tags=["User Login"])
api_router.include_router(user.endpoints_router, tags=["User Endpoints"])

api_router.include_router(employee.login_router, tags=["Employee Login"])
api_router.include_router(employee.endpoints_router, tags=["Employee Endpoints"])

api_router.include_router(client.login_router, tags=["Client Login"])
api_router.include_router(client.endpoints_router, tags=["Client Endpoints"])
