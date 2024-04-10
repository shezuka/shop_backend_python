from pydantic import BaseModel


class ResponseModelBase(BaseModel):
    __abstract__ = True


class ResponseModelOrmBase(ResponseModelBase):
    __abstract__ = True

    class Config:
        use_orm = True
        from_attributes = True
