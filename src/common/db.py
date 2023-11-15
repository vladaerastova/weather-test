from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class TemperatureRecord(Base):
    __tablename__ = 'temperature_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(255))
    temperature = Column(Float)
    timestamp = Column(DateTime)


url = os.getenv("DB_URL")
engine = create_engine(url)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_db():
    """Create session for database connection"""
    session = Session()
    try:
        yield session
    finally:
        session.close()
