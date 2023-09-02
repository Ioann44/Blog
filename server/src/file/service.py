import os
import uuid
from sqlalchemy.orm import joinedload

from . import entities
from ..common.base_class import Session, env


def __create_db_record(file: entities.File) -> entities.File | None:
    with Session() as session:
        saved = session.merge(file)
        session.commit()
        assert saved is not None, "File not saved to database"
        saved_detached: entities.File | None = (
            session.query(entities.File).options(joinedload(entities.File.post)).get(saved.id)
        )
        if saved_detached and saved_detached.post:
            saved_detached.post.id
        return saved_detached


def save_file(file) -> entities.File | None:
    """
    Args:
        file (FileStorage)
    """
    file.filename = f"{uuid.uuid4()}_{file.filename}"

    parent_path = env["UPLOADS_RESOLVED_PATH"]
    assert parent_path is not None, "Unresolved uploads path"
    full_path_with_name = os.path.join(parent_path, file.filename)
    file.save(full_path_with_name)

    try:
        return __create_db_record(entities.File(name=file.filename))
    # except:
    except Exception as e:
        os.remove(full_path_with_name)
        print(e)


# must be no accessible from client and executes regularly
def delete(id: int):
    with Session() as session:
        session.query(entities.File).filter_by(id=id).delete()
        session.commit()


def check_file_exists(name: str) -> bool:
    with Session() as session:
        file = session.query(entities.File).filter_by(name=name).first()
        return file is not None
