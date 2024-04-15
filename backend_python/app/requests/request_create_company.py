from typing import Optional

from pydantic import Field

from backend_python.app.requests.request_model_base import RequestModelBase


class RequestCreateCompany(RequestModelBase):
    name: str = Field("", min_length=1)
    logo_id: Optional[int] = Field(None, ge=0)
    description: str = Field(None, min_length=1)
