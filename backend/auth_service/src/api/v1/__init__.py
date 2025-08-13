from fastapi import APIRouter

from core.settings import settings
from api.v1.auth import router as auth_router
from api.v1.health import router as health_router


router = APIRouter(prefix=settings.project.api_v1)

router.include_router(router=auth_router)
router.include_router(router=health_router)
