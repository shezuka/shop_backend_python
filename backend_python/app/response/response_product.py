from backend_python.app.response.response_model_base import ResponseModelOrmBase


class ResponseProduct(ResponseModelOrmBase):
    name: str
    description: str
    category_id: int
    company_id: int
    image_id: int
