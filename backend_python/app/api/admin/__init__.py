from fastapi import APIRouter

from backend_python.app.api.admin.auth import admin_auth_router

admin_router = APIRouter()

admin_router.include_router(admin_auth_router, prefix="/auth", tags=["auth"])
