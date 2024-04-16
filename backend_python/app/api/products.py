from fastapi import APIRouter

from backend_python.app.helpers.crud import make_crud_router, CrudHandlerBase
from backend_python.app.response.response_product import ResponseProduct
from backend_python.database import ProductModel


class ProductsCrudHandler(CrudHandlerBase):
    DatabaseModel = ProductModel
    ResponseModel = ResponseProduct

    search_query_field = "name"

    create_api = False
    edit_api = False
    delete_api = False


products_router = APIRouter()
make_crud_router(
    products_router,
    ProductsCrudHandler
)
