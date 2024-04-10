from sqlalchemy import LargeBinary, Column
from sqlalchemy.orm import relationship

from backend_python.database.model_base import ModelBase


class ImageModel(ModelBase):
    __tablename__ = "images"

    binary_data = Column(LargeBinary, nullable=False)
    shopping_categories = relationship("ShoppingCategoryModel", back_populates="icon")
