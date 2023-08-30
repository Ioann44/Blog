import json
import pathlib
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
from . import entities

env = dotenv_values(pathlib.Path(__name__).parent.parent.joinpath("docker/.env").resolve())
db_url = env["DATABASE_URL"]
assert db_url is not None, "DATABASE_URL is not defined"

engine = create_engine(db_url)
entities.init(engine)
Session = sessionmaker(bind=engine)


def get_all() -> List[entities.Post]:
    with Session() as session:
        return session.query(entities.Post).order_by(entities.Post.id).all()


# insert or update
def save(post: entities.Post):
    with Session() as session:
        session.merge(post)
        session.commit()


def delete(id):
    with Session() as session:
        session.query(entities.Post).filter_by(id=id).delete()
        session.commit()
