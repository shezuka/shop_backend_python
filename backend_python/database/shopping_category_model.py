from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend_python.database.model_base import ModelBase


class ShoppingCategoryModel(ModelBase):
    __tablename__ = "shopping_categories"

    title = Column(String, unique=True, nullable=False)
    short_description = Column(String, nullable=False)

    icon_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    icon = relationship("ImageModel", back_populates="shopping_categories")
