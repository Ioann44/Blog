import pathlib
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
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
        return (
            session.query(entities.Post)
            .options(joinedload(entities.Post.author))
            .order_by(entities.Post.id)
            .all()
        )


def get_author_of_post(id: int) -> int | None:
    with Session() as session:
        return (
            session.query(entities.Post.author_id)
            .options(joinedload(entities.Post.author))
            .filter_by(id=id)
            .scalar()
        )


# insert or update
def save(post: entities.Post) -> entities.Post | None:
    with Session() as session:
        merged_post = session.merge(post)
        session.commit()
        return session.query(entities.Post).options(joinedload(entities.Post.author)).get(merged_post.id)


def delete(id: int):
    with Session() as session:
        session.query(entities.Post).filter_by(id=id).delete()
        session.commit()


# # delete all
# with Session() as session:
#     session.query(entities.Post).delete()
#     session.commit()
