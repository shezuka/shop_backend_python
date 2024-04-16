import sqlalchemy
from fastapi import APIRouter
from sqlalchemy.orm import Session

from backend_python.app.helpers.crud import CrudHandlerBase, make_crud_router
from backend_python.app.requests.request_create_category import RequestCreateCategory
from backend_python.app.response.response_category import ResponseCategory
from backend_python.database import CategoryModel


class CategoriesCrudHandler(CrudHandlerBase):
    DatabaseModel = CategoryModel
    RequestCreateModel = RequestCreateCategory
    RequestEditModel = RequestCreateModel
    ResponseModel = ResponseCategory
    is_admin_only = True
    search_query_field = "title"

    def create_uniqueness_query(self) -> sqlalchemy.orm.Query | None:
        return self.db.query(CategoryModel).filter(
            CategoryModel.title == self.req_data.title,
            CategoryModel.parent_category_id == self.req_data.parent_category_id
        )


admin_categories_router = APIRouter()
make_crud_router(
    admin_categories_router,
    CategoriesCrudHandler
)
