from fastapi import APIRouter

from backend_python.app.api.auth import auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
