from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB URL => where the db is stored
SQLALCHEMY_DATABASE_URL = "sqlite:///./conversations.db"

# Create a DB engine => connects Python to the DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session => used to talk to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class => creating tables
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()