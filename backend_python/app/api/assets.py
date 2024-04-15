from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session

from backend_python.app.dependencies import get_db
from backend_python.database import AssetModel

assets_router = APIRouter()


@assets_router.get("/{asset_id}")
async def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset: AssetModel = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return Response(content=asset.data, media_type=asset.type)
