from typing import Tuple
from sqlalchemy.exc import IntegrityError
from . import entities

from ..common.session_and_env import Session


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


def get_name(id: int) -> str | None:
    with Session() as session:
        user = session.query(entities.User).get(id)
        if user:
            return user.name
        else:
            return None
