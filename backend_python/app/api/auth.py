from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend_python.app.dependencies import get_db
from backend_python.app.helpers.password import hash_password
from backend_python.app.requests.request_login import RequestLogin
from backend_python.app.requests.request_register import RequestRegister
from backend_python.app.response.response_user import ResponseUser
from backend_python.database import UserModel

auth_router = APIRouter()


@auth_router.post("/login")
async def login(login_req: RequestLogin):
    return "success"


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
