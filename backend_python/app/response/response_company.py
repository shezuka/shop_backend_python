from typing import Optional

from backend_python.app.response.response_model_base import ResponseModelOrmBase


class ResponseCompany(ResponseModelOrmBase):
    name: str
    logo_id: Optional[int]
    description: str
