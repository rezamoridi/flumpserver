from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship,join, joinedload

URL = "postgresql://postgres:1050@127.0.0.1:5432/fluttermusicapp"

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


