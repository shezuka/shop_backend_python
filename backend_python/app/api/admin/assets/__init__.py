from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from backend_python.app.dependencies import get_db
from backend_python.app.dependencies.user import require_current_admin_user
from backend_python.app.helpers.crud import CrudHandlerBase, make_crud_router
from backend_python.app.helpers.random import generate_random_string
from backend_python.app.response.response_asset import ResponseAsset
from backend_python.database import UserModel, AssetUploadKeyModel, AssetModel

admin_assets_router = APIRouter()


class AssetCrudHandler(CrudHandlerBase):
    DatabaseModel = AssetModel
    RequestCreateModel = None
    RequestEditModel = None
    ResponseModel = ResponseAsset
    is_admin_only = True
    search_query_field = None


make_crud_router(
    admin_assets_router,
    AssetCrudHandler
)


@admin_assets_router.get("/upload-link")
async def get_upload_link(db: Session = Depends(get_db),
                          current_admin_user: UserModel = Depends(require_current_admin_user)):
    upload_key = generate_random_string(20)
    key = AssetUploadKeyModel()
    key.key = upload_key
    db.add(key)
    db.commit()
    return {"key": upload_key}


@admin_assets_router.post("/upload")
async def upload_asset(key: str = Query(...),
                       type: str = Query(...),
                       file: UploadFile = File(...),
                       db: Session = Depends(get_db),
                       current_admin_user: UserModel = Depends(require_current_admin_user)):
    key = db.query(AssetUploadKeyModel).filter(AssetUploadKeyModel.key == key).first()
    if not key:
        raise HTTPException(status_code=400, detail="Invalid key")

    db.query(AssetUploadKeyModel).filter(AssetUploadKeyModel.id == key.id).delete()

    asset = AssetModel()
    asset.type = type
    asset.data = await file.read()
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return {"asset_id": asset.id}
