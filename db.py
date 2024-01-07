

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://postgres:wzas1212@localhost:5000/hw11"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
