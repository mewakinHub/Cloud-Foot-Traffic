from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Config(Base):
    __tablename__ = "Config"
    username = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    Monitoring_status = Column(Integer, nullable=False)
    streaming_URL = Column(String, nullable=True)
    email = Column(String, nullable=True)

class Result(Base):
    __tablename__ = "Result"
    result_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    DATE_TIME = Column(DateTime, nullable=False)
    config = Column(String, nullable=True)
    result = Column(Integer, nullable=False)
    processed_detection_image = Column(Text, nullable=True)