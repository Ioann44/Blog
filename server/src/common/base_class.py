from sqlalchemy.orm import DeclarativeBase as __DBase


class Base(__DBase):
    pass


def __init():
    import pathlib
    from dotenv import dotenv_values
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    env = dotenv_values(pathlib.Path(__name__).parent.parent.joinpath(".env").resolve())
    uploads_path = env["UPLOADS_FOLDER"]
    assert uploads_path is not None, "UPLOADS_FOLDER is not defined"
    env["UPLOADS_RESOLVED_PATH"] = (
        pathlib.Path(__name__).parent.joinpath("server").joinpath(uploads_path).resolve().__str__()
    )
    db_url = env["DATABASE_URL"]
    assert db_url is not None, "DATABASE_URL is not defined"

    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    return sessionmaker(bind=engine), env


# Called only once
Session, env = __init()
