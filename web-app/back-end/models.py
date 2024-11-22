from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Result(Base):
    __tablename__ = 'Result'

    result_id = Column(Integer, primary_key=True, nullable=False,  autoincrement=True)
    username = Column(String(255), ForeignKey('Config.username'), nullable=False)
    DATE_TIME = Column(DateTime, nullable=False)
    config = Column(String(255), nullable=True)
    result = Column(Integer, nullable=False)
    processed_detection_image = Column(Text, nullable=False)

    # Relationship to the User table to access the related user
    user = relationship("Config", back_populates="data_entries")

class Config(Base):
    __tablename__ = 'Config'

    username = Column(String(255), primary_key=True, nullable=False)
    Monitoring_status = Column(Integer, nullable=False)
    streaming_URL = Column(Text, nullable=False)
    email = Column(String(255))

    # Relationship to the Data table for accessing related data entries
    data_entries = relationship("Result", back_populates="user")

