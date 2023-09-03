from typing import List, Tuple
from sqlalchemy import and_, exists, or_
from sqlalchemy.orm import joinedload

from . import entities
from ..file import entities as file_entities
from ..file import service as file_service
from ..common.base_class import Session


def get_all(user_id: int = 0) -> List[Tuple[entities.Post, bool]]:
    with Session() as session:
        like_exists = (
            exists()
            .where(
                and_(
                    entities.Post.id == entities.Like.post_id,
                    entities.Like.user_id == user_id,
                )
            )
            .label("like_exists")
        )

        query_result = (
            session.query(entities.Post, like_exists)
            .options(joinedload(entities.Post.author), joinedload(entities.Post.files))
            .order_by(entities.Post.id)
            .all()
        )

        return [(post, like_exists) for post, like_exists in query_result]


def get_author_of_post(id: int) -> int | None:
    with Session() as session:
        return session.query(entities.Post.author_id).filter_by(id=id).scalar()


# insert or update
def save(post: entities.Post) -> entities.Post | None:
    with Session() as session:
        merged_post = session.merge(post)
        session.commit()
        saved: entities.Post | None = (
            session.query(entities.Post).options(joinedload(entities.Post.author)).get(merged_post.id)
        )
        if saved:
            saved.author.name  # for 'await' lazy attribute (otherwise fails on call with already closed session)
        return saved


def delete(id: int):
    with Session() as session:
        post: entities.Post | None = session.query(entities.Post).get(id)
        if post is not None:
            # cascade deletion doesn't work, this is an option how to deal with it
            for file in post.files:
                session.delete(file)
            session.delete(post)
            session.commit()


def change_likes(user_id: int, post_id: int) -> Tuple[bool, int]:
    like_dict = {"user_id": user_id, "post_id": post_id}
    with Session() as session:
        is_liked = session.query(entities.Like).get(like_dict)
        if is_liked:
            session.query(entities.Like).filter_by(**like_dict).delete()
        else:
            session.add(entities.Like(**like_dict))

        post: entities.Post | None = session.query(entities.Post).get(post_id)
        if post:
            post.likes += -1 if is_liked else 1  # type: ignore
        session.commit()

        return not is_liked, post.likes  # type: ignore


def change_connected_post(filenames: List[str], post_id: int) -> List[str] | None:
    with Session() as session:
        post: entities.Post | None = session.query(entities.Post).get(post_id)
        assert post is not None, "Post not found"
        try:
            files_to_remove = [file for file in post.files if file.name not in filenames]
            for file in files_to_remove:
                post.files.remove(file)
                session.delete(file)

            current_filenames = [file.name for file in post.files]
            for fname in filenames:
                if fname not in current_filenames:
                    existing_file: file_entities.File | None = (
                        session.query(file_entities.File)
                        .filter_by(name=fname)
                        .filter(
                            or_(file_entities.File.post_id == None, file_entities.File.post_id == post_id)
                        )
                        .first()
                    )
                    assert existing_file, "Available file not exists"
                    post.files.append(existing_file)

            session.commit()
            # file_service.delete_files(*[file.name for file in files_to_remove]) # not needed because of session.delete(file)
            return [file.name for file in post.files]

        except Exception as e:
            session.rollback()
            print(e)


# # delete all
# with Session() as session:
#     session.query(entities.Post).delete()
#     session.commit()
