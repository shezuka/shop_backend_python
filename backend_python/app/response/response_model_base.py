import datetime

from pydantic import BaseModel


class ResponseModelBase(BaseModel):
    __abstract__ = True


class ResponseModelOrmBase(ResponseModelBase):
    __abstract__ = True

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        use_orm = True
        from_attributes = True
