import pathlib
from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import dotenv_values
from . import entities

env = dotenv_values(pathlib.Path(__name__).parent.parent.joinpath("docker/.env").resolve())
db_url = env["DATABASE_URL"]
assert db_url is not None, "DATABASE_URL is not defined"

engine = create_engine(db_url)
entities.init(engine)
Session = sessionmaker(bind=engine)


def create_user(user: entities.User) -> Tuple[bool, int]:
    with Session() as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return True, user.id  # type: ignore
            # return True, user.__dict__['id'] # alternative without type warning
        except IntegrityError:
            return False, 0


def get_user(name: str) -> Tuple[bool, entities.User | None]:
    with Session() as session:
        found_user = session.query(entities.User).filter_by(name=name).first()
        if found_user:
            return True, found_user
        else:
            return False, None


def check_name_availability(name: str) -> bool:
    with Session() as session:
        user = session.query(entities.User).filter_by(name=name).first()
        return user is None
