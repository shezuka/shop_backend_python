from backend_python.app.requests.request_model_base import RequestModelBase


class RequestLogin(RequestModelBase):
    username: str
    password: str
