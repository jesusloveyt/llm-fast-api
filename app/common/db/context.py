from os import getenv

from typing import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from common.constants import DB_CONNECTION_STRING

if not DB_CONNECTION_STRING:
    raise Exception("DB connection string not providet")

engine = create_engine(DB_CONNECTION_STRING, echo=False, pool_pre_ping=True, pool_recycle=3600)  # reconect after 1 hour
session_maker = sessionmaker(bind=engine, expire_on_commit=False)

def get_db() -> Generator[Session, Any, None]:
    with session_maker() as session:
        yield session