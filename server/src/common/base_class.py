from sqlalchemy.orm import DeclarativeBase as __DBase


class Base(__DBase):
    pass


def __init():
    import pathlib
    from dotenv import dotenv_values
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    env = dotenv_values(pathlib.Path(__name__).parent.parent.joinpath("docker/.env").resolve())
    db_url = env["DATABASE_URL"]
    assert db_url is not None, "DATABASE_URL is not defined"

    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    return sessionmaker(bind=engine), env


# Called only once
Session, env = __init()
