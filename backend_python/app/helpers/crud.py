from typing import Type, Optional, Union

import sqlalchemy
from fastapi import APIRouter, Response, Depends, HTTPException, Request
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from backend_python.app.dependencies import get_db
from backend_python.app.dependencies.query import get_query_array_int
from backend_python.app.dependencies.user import get_current_user, require_current_admin_user
from backend_python.app.requests.request_model_base import RequestModelBase
from backend_python.app.response.response_model_base import ResponseModelOrmBase
from backend_python.database import UserModel
from backend_python.database.model_base import ModelBase


class CrudHandlerBase:
    __abstract__ = True
    search_query_field: str
    is_admin_only: bool = False
    DatabaseModel: Type[ModelBase]
    RequestCreateModel: Type[RequestModelBase]
    RequestEditModel: Type[RequestModelBase]
    ResponseModel: Type[ResponseModelOrmBase]

    def __init__(self, current_user: UserModel = None, req_data: RequestModelBase = None, db: Session = None):
        self.current_user: UserModel = current_user
        self.req_data: RequestModelBase = req_data
        self.db: Session = db

    def create_uniqueness_query(self) -> sqlalchemy.orm.Query | None:
        return None

    def create_new_model_instance(self):
        return self.DatabaseModel(**self.req_data.dict())


def make_crud_router(router: APIRouter,
                     handler_class: Type[CrudHandlerBase]):
    @router.post("")
    async def create_query(req: handler_class.RequestCreateModel,
                           response: Response,
                           db: Session = Depends(get_db),
                           current_user=Depends(get_current_user)):
        if handler_class.is_admin_only:
            await require_current_admin_user(current_user)

        handler = handler_class(
            current_user=current_user,
            req_data=req,
            db=db
        )

        old_item = handler.create_uniqueness_query().first()
        if old_item is not None:
            response.status_code = 400
            return {"message": "such item already exists"}

        new_item = handler.create_new_model_instance()
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return handler.ResponseModel.from_orm(new_item)

    @router.get("")
    async def get_query(
            request: Request,
            response: Response,
            offset: int = 0,
            limit: int = 10,
            q: Optional[str] = None,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if handler_class.is_admin_only:
            await require_current_admin_user(current_user)

        handler = handler_class(
            current_user=current_user,
            db=db
        )
        except_ids = get_query_array_int(request, "except_ids")

        base_query = db.query(handler_class.DatabaseModel)
        query = base_query.order_by(handler_class.DatabaseModel.id.desc())
        if handler_class.search_query_field is not None and q is not None:
            query = query.filter(
                sqlalchemy.func.lower(getattr(handler_class.DatabaseModel, handler_class.search_query_field))
                .like('%{}%'.format(q.lower()))
            )
        if except_ids is not None and len(except_ids) > 0:
            query = query.filter(handler_class.DatabaseModel.id.notin_(except_ids))
        categories = query.limit(limit).offset(offset).all()
        total_count = base_query.count()
        response.headers["X-Total-Count"] = str(total_count)
        return parse_obj_as(list[handler_class.ResponseModel], categories)

    @router.get("/{id}")
    async def get_one_query(id: int, db: Session = Depends(get_db)):
        item = db.query(handler_class.DatabaseModel).filter(handler_class.DatabaseModel.id == id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="item not found")
        return handler_class.ResponseModel.from_orm(item)

    @router.put("/{id}")
    async def update_query(
            id: int,
            req: handler_class.RequestEditModel,
            response: Response,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if handler_class.is_admin_only:
            await require_current_admin_user(current_user)

        handler = handler_class(
            current_user=current_user,
            req_data=req,
            db=db
        )
        other_item = handler.create_uniqueness_query().filter(handler_class.DatabaseModel.id != id).first()
        if other_item is not None:
            response.status_code = 400
            return {"message": "such item already exists"}

        item = db.query(handler_class.DatabaseModel).filter(handler_class.DatabaseModel.id == id).first()
        if item is None:
            response.status_code = 404
            return {"message": "item not found"}

        for key, value in req.dict().items():
            setattr(item, key, value)
        db.add(item)
        db.commit()
        db.refresh(item)
        return handler_class.ResponseModel.from_orm(item)

    @router.delete("/{id}")
    async def delete_query(
            id: int,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if handler_class.is_admin_only:
            await require_current_admin_user(current_user)
        db.query(handler_class.DatabaseModel).filter(handler_class.DatabaseModel.id == id).delete()
        db.commit()
        return {"message": "item deleted"}
