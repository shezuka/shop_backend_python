from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend_python.app.dependencies import get_db
from backend_python.app.helpers.password import hash_password, verify_password
from backend_python.app.helpers.random import generate_random_string
from backend_python.app.requests.request_login import RequestLogin
from backend_python.app.requests.request_register import RequestRegister
from backend_python.app.response.response_access_token import ResponseAccessToken
from backend_python.app.response.response_user import ResponseUser
from backend_python.database import UserModel, AccessTokenModel

auth_router = APIRouter()


@auth_router.post("/login", status_code=200)
async def login(login_req: RequestLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == login_req.username).first()
    if user is None:
        response.status_code = 400
        return {"message": "username does not exist"}

    if not verify_password(login_req.password, user.encrypted_password):
        response.status_code = 400
        return {"message": "invalid password"}

    token = generate_random_string()
    access_token = AccessTokenModel(user_id=user.id, key=token)
    db.add(access_token)
    db.commit()
    db.refresh(access_token)
    return ResponseAccessToken.from_orm(access_token)


@auth_router.post("/register", status_code=201)
async def register(register_req: RequestRegister, response: Response, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == register_req.username).first()
    if user is not None:
        response.status_code = 400
        return {"message": "username already exists"}

    new_user = UserModel()
    new_user.username = register_req.username
    new_user.encrypted_password = hash_password(register_req.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return ResponseUser.from_orm(new_user)
