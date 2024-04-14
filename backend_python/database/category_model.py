from sqlalchemy import String, Column, Integer, ForeignKey

from backend_python.database.model_base import ModelBase


class CategoryModel(ModelBase):
    __tablename__ = "categories"

    title = Column(String, unique=True, nullable=False)
    parent_category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
