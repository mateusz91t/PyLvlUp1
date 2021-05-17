from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# I don't need it after set SQLALCHEMY_DATABASE_URL=postgres....
# engine = create_engine("postgresql://postgres:DaftAcademy@127.0.0.1:5555/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency?
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
