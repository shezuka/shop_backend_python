from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend_python.database.model_base import ModelBase


class ProductModel(ModelBase):
    __tablename__ = "products"

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("CategoryModel")

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("CompanyModel")

    image_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    image = relationship("AssetModel")

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
