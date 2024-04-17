from fastapi import APIRouter

from backend_python.app.helpers.crud import make_crud_router, CrudHandlerBase
from backend_python.app.response.response_company import ResponseCompany
from backend_python.database import CompanyModel


class CompaniesCrudHandler(CrudHandlerBase):
    DatabaseModel = CompanyModel
    ResponseModel = ResponseCompany

    search_query_field = "name"

    create_api = False
    edit_api = False
    delete_api = False


companies_router = APIRouter()
make_crud_router(
    companies_router,
    CompaniesCrudHandler
)
