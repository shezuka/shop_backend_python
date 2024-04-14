import sqlalchemy
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend_python.app.dependencies import get_db
from backend_python.app.dependencies.access_token import get_access_token
from backend_python.database import AccessTokenModel, UserModel


async def get_current_user(db: Session = Depends(get_db),
                           access_token: str = Depends(get_access_token)):
    return (
        db.query(UserModel)
        .join(AccessTokenModel,
              sqlalchemy.and_(AccessTokenModel.user_id == UserModel.id, AccessTokenModel.key == access_token))
        .first()
    )


async def require_current_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return current_user


async def get_current_admin_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user or not current_user.is_full_admin:
        return None
    return current_user


async def require_current_admin_user(admin_user: UserModel = Depends(get_current_admin_user)):
    if not admin_user or not admin_user.is_full_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return admin_user
