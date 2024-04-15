import sqlalchemy
from fastapi import APIRouter, Response, Depends, HTTPException
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from backend_python.app.dependencies import get_db
from backend_python.app.dependencies.user import get_current_user, require_current_admin_user


class CrudHandlerBase:
    __abstract__ = True
    DatabaseModel = None

    def create_uniqueness_query(self, db: Session, req_data: any) -> sqlalchemy.orm.Query | None:
        return None

    def create_new_model_instance(self, req_data: any) -> DatabaseModel:
        return self.DatabaseModel(**req_data.dict())


def make_crud_router(router: APIRouter,
                     ResponseModel,
                     DatabaseModel,
                     CreateRequestModel,
                     handler: CrudHandlerBase,
                     is_admin_only: bool = False):
    @router.post("")
    async def create_query(req: CreateRequestModel,
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

    @router.get("/{id}")
    async def get_one_query(id: int, db: Session = Depends(get_db)):
        item = db.query(DatabaseModel).filter(DatabaseModel.id == id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="item not found")
        return ResponseModel.from_orm(item)

    @router.put("/{id}")
    async def update_query(
            id: int,
            req: CreateRequestModel,
            response: Response,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if is_admin_only:
            await require_current_admin_user(current_user)

        other_item = handler.create_uniqueness_query(db, req).filter(DatabaseModel.id != id).first()
        if other_item is not None:
            response.status_code = 400
            return {"message": "such item already exists"}

        item = db.query(DatabaseModel).filter(DatabaseModel.id == id).first()
        if item is None:
            response.status_code = 404
            return {"message": "item not found"}

        for key, value in req.dict().items():
            setattr(item, key, value)
        db.add(item)
        db.commit()
        db.refresh(item)
        return ResponseModel.from_orm(item)

    @router.delete("/{id}")
    async def delete_query(
            id: int,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)
    ):
        if is_admin_only:
            await require_current_admin_user(current_user)
        db.query(DatabaseModel).filter(DatabaseModel.id == id).delete()
        db.commit()
        return {"message": "item deleted"}
