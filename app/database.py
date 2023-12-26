import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#! Note: SqlAlchemy uses psycopg2 under-the-hood

DB_USER = os.environ["DATABASE_USER"]
DB_PW = os.environ["DATABASE_PASSWORD"]
DB_HOST = os.environ["DATABASE_HOST"]
DB_NAME = os.environ["DATABASE"]
DB_PORT = os.environ["DATABASE_PORT"]

DB_CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency``
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
