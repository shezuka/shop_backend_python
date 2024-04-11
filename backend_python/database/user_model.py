from datetime import datetime

from sqlalchemy import String, Column, DateTime, Boolean
from sqlalchemy.orm import relationship

from backend_python.database.model_base import ModelBase


class UserModel(ModelBase):
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    encrypted_password = Column(String, nullable=False)
    access_tokens = relationship("AccessTokenModel", back_populates="user")
    is_full_admin = Column(Boolean, default=False)
