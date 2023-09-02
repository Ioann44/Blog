from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..common.base_class import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)

    post = relationship("Post", back_populates="files")
