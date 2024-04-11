from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend_python.app.dependencies import get_db
from backend_python.app.helpers.password import verify_password
from backend_python.app.helpers.random import generate_random_string
from backend_python.app.requests.request_login import RequestLogin
from backend_python.app.response.response_access_token import ResponseAccessToken
from backend_python.database import UserModel, AccessTokenModel

admin_auth_router = APIRouter()


@admin_auth_router.post("/login", status_code=200)
def login(login_req: RequestLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == login_req.username).first()
    if user is None or not verify_password(login_req.password, user.encrypted_password) or not user.is_full_admin:
        response.status_code = 400
        return {"message": "invalid credentials"}

    token = generate_random_string()
    access_token = AccessTokenModel(user_id=user.id, key=token)
    db.add(access_token)
    db.commit()
    db.refresh(access_token)
    return ResponseAccessToken.from_orm(access_token)
