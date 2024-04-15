from sqlalchemy import String, Column

from .model_base import ModelBase


class AssetUploadKeyModel(ModelBase):
    __tablename__ = 'asset_upload_keys'

    key: str = Column(String)
