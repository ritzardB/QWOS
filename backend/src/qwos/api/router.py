from fastapi import APIRouter

from qwos.api.routers.health_router import router as health_router
from qwos.api.routers.hr_router import router as hr_router
from qwos.api.routers.identity_router import router as identity_router

api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(health_router)
api_router.include_router(identity_router)
api_router.include_router(hr_router)