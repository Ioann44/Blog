from sqlalchemy import ARRAY, DateTime, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # make it foreign
    author_id = Column(Integer, ForeignKey("users.id"))
    theme = Column(String)
    content = Column(ARRAY(String))
    likes = Column(Integer, default=0)
    date = Column(DateTime(timezone=True), server_default=func.now())

    author = relationship("User", back_populates="posts")


def init(engine):
    Base.metadata.create_all(engine)
