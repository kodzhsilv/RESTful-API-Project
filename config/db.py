from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the connection URL to the MySQL database
DATABASE_URL = "mysql+pymysql://root123:none@localhost:3306/car_maintenance_api"

# Create the base class for the ORM models
Base = declarative_base()

# Create the SQLAlchemy engine to connect to the database
engine = create_engine(DATABASE_URL)

# Create the session maker to handle database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
