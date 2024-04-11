from pydantic import Field

from backend_python.app.requests.request_model_base import RequestModelBase


class RequestValidateToken(RequestModelBase):
    token: str = Field(min_length=1)
