from typing import Optional

from backend_python.app.response.response_model_base import ResponseModelOrmBase


class ResponseCategory(ResponseModelOrmBase):
    title: str
    parent_category_id: Optional[int]
    image_id: Optional[int]
