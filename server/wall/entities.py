from sqlalchemy import ARRAY, DateTime, Column, Integer, String, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # make it foreign
    author_id = Column(Integer, nullable=False)
    theme = Column(String, nullable=False)
    content = Column(ARRAY(String), nullable=False)
    likes = Column(Integer, default=0)
    date = Column(DateTime(timezone=True), server_default=func.now())


def init(engine):
    Base.metadata.create_all(engine)
