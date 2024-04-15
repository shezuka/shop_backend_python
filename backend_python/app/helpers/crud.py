from typing import Type, Optional

import sqlalchemy
from fastapi import APIRouter, Response, Depends, HTTPException, Request
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from backend_python.app.dependencies import get_db
from backend_python.app.dependencies.query import get_query_array_int
from backend_python.app.dependencies.user import get_current_user, require_current_admin_user
from backend_python.app.requests.request_model_base import RequestModelBase
from backend_python.app.response.response_model_base import ResponseModelOrmBase
from backend_python.database.model_base import ModelBase


class CrudHandlerBase:
    __abstract__ = True
    DatabaseModel = None

    def create_uniqueness_query(self, db: Session, req_data: any) -> sqlalchemy.orm.Query | None:
        return None

    def create_new_model_instance(self, req_data: any) -> DatabaseModel:
        return self.DatabaseModel(**req_data.dict())


def make_crud_router(router: APIRouter,
                     response_model: Type[ResponseModelOrmBase],
                     database_model: Type[ModelBase],
                     create_request_model: Type[RequestModelBase],
                     edit_request_model: Type[RequestModelBase],
                     handler: CrudHandlerBase,
                     search_query_field: str = None,
                     is_admin_only: bool = False):
    @router.post("")
    async def create_query(req: create_request_model,
                           response: Response,
                           db: Session = Depends(get_db),
                           current_user=Depends(get_current_user)):
        if is_admin_only:
            await require_current_admin_user(current_user)

        old_item = handler.create_uniqueness_query(db, req).first()
        if old_item is not None:
            response.status_code = 400
            return {"message": "such item already exists"}

        new_item = handler.create_new_model_instance(req)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return response_model.from_orm(new_item)

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
        if is_admin_only:
            await require_current_admin_user(current_user)

        except_ids = get_query_array_int(request, "except_ids")

        base_query = db.query(database_model)
        query = base_query.order_by(database_model.id.desc())
        if search_query_field is not None and q is not None:
            query = query.filter(getattr(database_model, search_query_field).like('%{}%'.format(q)))
        if except_ids is not None and len(except_ids) > 0:
            query = query.filter(database_model.id.notin_(except_ids))
        categories = query.limit(limit).offset(offset).all()
        total_count = base_query.count()
        response.headers["X-Total-Count"] = str(total_count)
        return parse_obj_as(list[response_model], categories)

    @router.get("/{id}")
    async def get_one_query(id: int, db: Session = Depends(get_db)):
        item = db.query(database_model).filter(database_model.id == id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="item not found")
        return response_model.from_orm(item)

    @router.put("/{id}")
    async def update_query(
            id: int,
            req: edit_request_model,
            response: Response,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if is_admin_only:
            await require_current_admin_user(current_user)

        other_item = handler.create_uniqueness_query(db, req).filter(database_model.id != id).first()
        if other_item is not None:
            response.status_code = 400
            return {"message": "such item already exists"}

        item = db.query(database_model).filter(database_model.id == id).first()
        if item is None:
            response.status_code = 404
            return {"message": "item not found"}

        for key, value in req.dict().items():
            setattr(item, key, value)
        db.add(item)
        db.commit()
        db.refresh(item)
        return response_model.from_orm(item)

    @router.delete("/{id}")
    async def delete_query(
            id: int,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if is_admin_only:
            await require_current_admin_user(current_user)
        db.query(database_model).filter(database_model.id == id).delete()
        db.commit()
        return {"message": "item deleted"}
