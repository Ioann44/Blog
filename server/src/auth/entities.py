from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..common.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="author")
