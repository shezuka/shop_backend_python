from pydantic import Field

from backend_python.app.requests.request_model_base import RequestModelBase


class RequestRegister(RequestModelBase):
    username: str = Field(None, min_length=4)
    password: str = Field(None, min_length=6)
