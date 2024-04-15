import sqlalchemy
from fastapi import APIRouter
from sqlalchemy.orm import Session

from backend_python.app.helpers.crud import CrudHandlerBase, make_crud_router
from backend_python.app.requests.request_create_company import RequestCreateCompany
from backend_python.app.response.response_company import ResponseCompany
from backend_python.database import CompanyModel


class CompaniesCrudHandler(CrudHandlerBase):
    DatabaseModel = CompanyModel

    def create_uniqueness_query(self, db: Session, req_data: any) -> sqlalchemy.orm.Query | None:
        return db.query(CompanyModel).filter(CompanyModel.name == req_data.name)


admin_companies_router = APIRouter()
make_crud_router(
    admin_companies_router,
    ResponseCompany,
    CompanyModel,
    RequestCreateCompany,
    RequestCreateCompany,
    CompaniesCrudHandler(),
    search_query_field="name",
    is_admin_only=True
)
