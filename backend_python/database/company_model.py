from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend_python.database.model_base import ModelBase


class CompanyModel(ModelBase):
    __tablename__ = "companies"

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    logo_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    logo = relationship("AssetModel")
