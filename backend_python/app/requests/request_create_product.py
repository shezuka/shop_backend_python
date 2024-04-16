from pydantic import Field

from backend_python.app.requests.request_model_base import RequestModelBase


class RequestCreateProduct(RequestModelBase):
    name: str = Field("", min_length=1)
    description: str = Field("", min_length=1)
    category_id: int = Field(None, ge=0)
    company_id: int = Field(None, ge=0)
    image_id: int = Field(None, ge=0)
