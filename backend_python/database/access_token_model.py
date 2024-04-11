from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from backend_python.database.model_base import ModelBase


class AccessTokenModel(ModelBase):
    __tablename__ = 'access_tokens'

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserModel', back_populates='access_tokens')
    key = Column(String, unique=True, nullable=False)
    expiration_datetime = Column(Integer, nullable=True)
