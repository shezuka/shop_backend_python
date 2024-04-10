import datetime

from backend_python.app.response.response_model_base import ResponseModelOrmBase


class ResponseUser(ResponseModelOrmBase):
    id: int
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
