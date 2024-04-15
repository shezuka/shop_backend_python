from fastapi import APIRouter

from backend_python.app.api.admin.assets import admin_assets_router
from backend_python.app.api.admin.auth import admin_auth_router
from backend_python.app.api.admin.categories import admin_categories_router

admin_router = APIRouter()

admin_router.include_router(admin_auth_router, prefix="/auth", tags=["auth"])
admin_router.include_router(admin_categories_router, prefix="/categories", tags=["categories"])
admin_router.include_router(admin_assets_router, prefix="/assets", tags=["assets"])