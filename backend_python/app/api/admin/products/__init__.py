import sqlalchemy
from fastapi import APIRouter
from sqlalchemy.orm import Session

from backend_python.app.helpers.crud import CrudHandlerBase, make_crud_router
from backend_python.app.requests.request_create_product import RequestCreateProduct
from backend_python.app.response.response_product import ResponseProduct
from backend_python.database import ProductModel


class ProductsCrudHandler(CrudHandlerBase):
    DatabaseModel = ProductModel
    RequestCreateModel = RequestCreateProduct
    RequestEditModel = RequestCreateModel
    ResponseModel = ResponseProduct
    is_admin_only = True
    search_query_field = "name"

    def create_uniqueness_query(self) -> sqlalchemy.orm.Query | None:
        return self.db.query(self.DatabaseModel).filter(self.DatabaseModel.name == self.req_data.name)


admin_products_router = APIRouter()
make_crud_router(
    admin_products_router,
    ProductsCrudHandler
)
