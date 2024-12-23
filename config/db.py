from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#connection URL to the MySQL database
DATABASE_URL = "mysql+pymysql://root123:none@localhost:3306/car_maintenance_api"

Base = declarative_base()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()