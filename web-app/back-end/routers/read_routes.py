from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db
from models import Result, Config
from datetime import datetime

router = APIRouter()

class ConfigModel(BaseModel):
    username: str
    Monitoring_status: int
    streaming_URL: str
    email: str | None = None

class ResultModel(BaseModel):
    username: str
    DATE_TIME: datetime
    config: str
    result: int | None = None

@router.get("/images_all", response_model=List[str])
def get_processed_images(db: Session = Depends(get_db)):
    # Query only the `processed_detection_image` column from the Result table
    processed_images = db.query(Result.processed_detection_image).all()

    # Extract the strings from the result tuples
    processed_images_list = [image[0] for image in processed_images]

    if not processed_images_list:
        raise HTTPException(status_code=404, detail="No processed detection images found")

    return processed_images_list

@router.get("/images/{username}", response_model=List[str])
def get_processed_images(username: str, db: Session = Depends(get_db)):
    # Query `processed_detection_image` column where `username` matches
    processed_images = db.query(Result.processed_detection_image).filter(Result.username == username).all()

    # Extract the strings from the result tuples
    processed_images_list = [image[0] for image in processed_images]

    if not processed_images_list:
        raise HTTPException(status_code=404, detail=f"No processed detection images found for username: {username}")

    return processed_images_list

@router.get("/configs", response_model=List[ConfigModel])
def get_all_configs(db: Session = Depends(get_db)):
    # Query all records from the Config table
    configs = db.query(Config).all()
    return configs

@router.get("/config/{username}", response_model=ConfigModel)
def get_config(username: str, db: Session = Depends(get_db)):
    # Query one record from the Config table
    config = db.query(Config).filter(Config.username == username).first()
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config

@router.get("/results/{username}", response_model=List[ResultModel])
def get_selected_results(username:str, db: Session = Depends(get_db)):
    # Query specific columns from the Result table
    results = (
        db.query(Result.username, Result.DATE_TIME, Result.config, Result.result)
        .filter(Result.username == username)
    )
    
    # Convert the query results into a list of dictionaries
    return [
        {
            "username": row.username,
            "DATE_TIME": row.DATE_TIME,
            "config": row.config,
            "result": row.result,
        }
        for row in results
    ]