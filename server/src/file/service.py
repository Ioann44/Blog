import os
import uuid
from sqlalchemy import event
from sqlalchemy.orm import joinedload

from . import entities
from ..common.session_and_env import Session, env


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


# doesn't work with rollback after failed inserting, so, manually deleting still needed in this case
@event.listens_for(entities.File, "before_delete")
def delete_files_listened(mapper, connection, target):
    delete_files(target.name)


# move function to different "export" file if needed more imports
def delete_files(*filenames: str):
    parent_path = env["UPLOADS_RESOLVED_PATH"]
    assert parent_path is not None, "Unresolved uploads path"
    for fname in filenames:
        full_path_with_name = os.path.join(parent_path, fname)
        try:
            os.remove(full_path_with_name)
        except Exception:
            # somehow file already deleted
            pass


def check_file_exists(name: str) -> bool:
    with Session() as session:
        file = session.query(entities.File).filter_by(name=name).first()
        return file is not None


def delete_unused_files():
    # may be covered with apscheduler
    with Session() as session:
        unused_files = session.query(entities.File).filter(entities.File.post_id.is_(None)).all()
        # print(f"{len(unused_files)} unused files deleted")
        for file in unused_files:
            delete_files(file.name)  # type: ignore
            session.delete(file)
        session.commit()


# # delete all
# with Session() as session:
#     session.query(entities.File).delete()
#     session.commit()
