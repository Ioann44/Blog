from sqlalchemy import ARRAY, DateTime, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from ..common.base_class import Base

# from ..auth.entities import User
# from ..file.entities import File


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    theme = Column(String)
    content = Column(ARRAY(String))
    likes = Column(Integer, default=0)
    date = Column(DateTime(timezone=True), server_default=func.now())

    author = relationship("User", back_populates="posts")
    authors_who_liked = relationship("User", secondary="likes", back_populates="liked_posts")
    files = relationship("File", back_populates="post")


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
