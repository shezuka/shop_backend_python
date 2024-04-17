from fastapi import APIRouter

from backend_python.app.helpers.crud import make_crud_router, CrudHandlerBase
from backend_python.app.response.response_category import ResponseCategory
from backend_python.database import CategoryModel


class CategoriesCrudHandler(CrudHandlerBase):
    DatabaseModel = CategoryModel
    ResponseModel = ResponseCategory

    search_query_field = "title"

    create_api = False
    edit_api = False
    delete_api = False


categories_router = APIRouter()
make_crud_router(
    categories_router,
    CategoriesCrudHandler
)
