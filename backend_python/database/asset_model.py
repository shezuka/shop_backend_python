from sqlalchemy import Column, String, LargeBinary

from .model_base import ModelBase


class AssetModel(ModelBase):
    __tablename__ = "assets"

    data = Column(LargeBinary, nullable=False)
    type = Column(String(255), nullable=False)
