from pydantic import BaseModel


class RequestModelBase(BaseModel):
    __abstract__ = True
