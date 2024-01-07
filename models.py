from sqlalchemy import create_engine, Column, Integer, String, Boolean
from db import Base, engine


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(150), unique=True, index=True)
    phone = Column(String(50), index=True)
    born_date = Column(String(50))
    description = Column(String(255), default=False, nullable=True)


Base.metadata.create_all(bind=engine)
