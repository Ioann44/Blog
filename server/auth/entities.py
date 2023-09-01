from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="author_id")


def init(engine):
    Base.metadata.create_all(engine)
