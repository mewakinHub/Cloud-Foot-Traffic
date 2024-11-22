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

@router.get("/configs", response_model=List[ConfigModel])
def get_all_configs(db: Session = Depends(get_db)):
    # Query all records from the Config table
    configs = db.query(Config).all()
    return configs

@router.get("/results", response_model=List[ResultModel])
def get_selected_results(db: Session = Depends(get_db)):
    # Query specific columns from the Result table
    results = (
        db.query(Result.username, Result.DATE_TIME, Result.config, Result.result)
        .all()
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
