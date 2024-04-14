import sqlalchemy
from fastapi import APIRouter, Response, Depends
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from backend_python.app.dependencies import get_db
from backend_python.app.dependencies.user import get_current_user, require_current_admin_user


class CrudHandlerBase[DatabaseModel]:
    __abstract__ = True

    def create_uniqueness_query(self, db: Session, req_data: any) -> sqlalchemy.orm.Query | None:
        return None

    def create_new_model_instance(self, req_data: any) -> DatabaseModel:
        return DatabaseModel(**req_data.dict())


def make_crud_router(router: APIRouter,
                     ResponseModel,
                     DatabaseModel,
                     CreateRequestModel,
                     handler: CrudHandlerBase,
                     is_admin_only: bool = False):
    @router.post("", response_model=list[ResponseModel])
    async def create_query(req: CreateRequestModel,
                           response: Response,
                           db: Session = Depends(get_db),
                           current_user=Depends(get_current_user)):
        if is_admin_only:
            await require_current_admin_user(current_user)

        old_item = handler.create_uniqueness_query(db, req)
        if old_item is not None:
            response.status_code = 400
            return {"message": "such item already exists"}

        new_item = handler.create_new_model_instance(req)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return ResponseModel.from_orm(new_item)

    @router.get("")
    async def get_query(
            response: Response,
            offset: int = 0,
            limit: int = 10,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if is_admin_only:
            await require_current_admin_user(current_user)

        base_query = db.query(DatabaseModel)
        categories = base_query.order_by(DatabaseModel.id.desc()).limit(limit).offset(offset).all()
        total_count = base_query.count()
        response.headers["X-Total-Count"] = str(total_count)
        return parse_obj_as(list[ResponseModel], categories)

    @router.put("/{id}", response_model=ResponseModel)
    async def update_query(
            id: int,
            req: CreateRequestModel,
            response: Response,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if is_admin_only:
            await require_current_admin_user(current_user)

        item = db.query(DatabaseModel).filter(DatabaseModel.id == id).first()
        if item is None:
            response.status_code = 404
            return {"message": "item not found"}

        old_item = handler.create_uniqueness_query(db, req).filter(DatabaseModel.id != id).first()
        if old_item is not None:
            response.status_code = 400
            return {"message": "such item already exists"}

        item.update(**req.dict())
        db.commit()
        db.refresh(item)
        return ResponseModel.from_orm(item)


    @router.delete("/{id}")
    async def delete_query(
            id: int,
            response: Response,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if is_admin_only:
            await require_current_admin_user(current_user)
        db.query(DatabaseModel).filter(DatabaseModel.id == id).delete()
        return {"message": "item deleted"}
