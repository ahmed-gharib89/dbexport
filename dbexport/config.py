import os
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@lru_cache(maxsize=32)
def engine(db_url=None):
    """Return an engine for the database .

    Args:
        db_url (string, optional): url for the database. Defaults to None.

    Raises:
        ValueError: database URL is required.

    Returns:
        engine: database engine object.
    """
    db_url = db_url or os.getenv("DB_URL")
    if not db_url:
        raise ValueError("database URL is required")
    print(f"Returning an engine for {db_url}")
    return create_engine(db_url)


def get_connection(db_url=None):
    """Get a connection to the database .

    Args:
        db_url (string, optional): url for the database. Defaults to None.

    Returns:
        connection: database engine connection object.
    """
    return engine(db_url).connect()


@lru_cache(maxsize=32)
def session_class(db_url=None):
    """Return a session class to use with SQLAlchemy engine .

    Args:
        db_url (string, optional): url for the database. Defaults to None.

    Returns:
        session: database engine session object.
    """
    return sessionmaker(bind=engine(db_url))


try:
    Session = session_class()
except:
    pass
