import sqlalchemy
from fastapi import APIRouter
from sqlalchemy.orm import Session

from backend_python.app.helpers.crud import CrudHandlerBase, make_crud_router
from backend_python.app.requests.request_create_category import RequestCreateCategory
from backend_python.app.response.response_category import ResponseCategory
from backend_python.database import CategoryModel


class CategoriesCrudHandler(CrudHandlerBase):
    DatabaseModel = CategoryModel

    def create_uniqueness_query(self, db: Session, req_data: any) -> sqlalchemy.orm.Query | None:
        return db.query(CategoryModel).filter(
            CategoryModel.title == req_data.title,
            CategoryModel.parent_category_id == req_data.parent_category_id
        )


admin_categories_router = APIRouter()
make_crud_router(
    admin_categories_router,
    ResponseCategory,
    CategoryModel,
    RequestCreateCategory,
    RequestCreateCategory,
    CategoriesCrudHandler(),
    search_query_field="title",
    is_admin_only=True
)
