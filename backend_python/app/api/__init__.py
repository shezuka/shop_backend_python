from fastapi import APIRouter

from backend_python.app.api.admin import admin_router
from backend_python.app.api.assets import assets_router
from backend_python.app.api.auth import auth_router
from backend_python.app.api.categories import categories_router
from backend_python.app.api.companies import companies_router
from backend_python.app.api.products import products_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(assets_router, prefix="/assets", tags=["assets"])
router.include_router(products_router, prefix="/products", tags=["products"])
router.include_router(companies_router, prefix="/companies", tags=["companies"])
router.include_router(categories_router, prefix="/categories", tags=["categories"])
