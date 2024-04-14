from typing import Optional

from pydantic import Field

from backend_python.app.requests.request_model_base import RequestModelBase


class RequestCreateCategory(RequestModelBase):
    title: str = Field("", min_length=1)
    parent_category_id: Optional[int] = Field(None, ge=0)
