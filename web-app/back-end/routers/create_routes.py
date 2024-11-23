from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Result, Config
import requests
import base64
from datetime import datetime

router = APIRouter()

# Schemas for Result Routes?
class Create_Result_RequestBody(BaseModel):
    username: str
    config: str | None = None
    result: int
    image_url: str

class Create_Config_RequestBody(BaseModel):
    username: str
    Monitoring_status: int
    streaming_URL: str
    email: str | None = None

# Routes
@router.post("/result")
def create_result(result_data: Create_Result_RequestBody, db: Session = Depends(get_db)):
    try:
        response = requests.get(result_data.image_url)
        response.raise_for_status()
        if "image/png" not in response.headers["Content-Type"]:
            raise HTTPException(status_code=400, detail="Invalid PNG image")
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image: {str(e)}")
    
    image_base64 = base64.b64encode(response.content).decode("utf-8")
    current_time = datetime.now()

    new_result = Result(
        username=result_data.username,
        DATE_TIME=current_time,
        config=result_data.config,
        result=result_data.result,
        processed_detection_image=image_base64,
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return (new_result)

@router.post("/config")
def create_config(config_data: Create_Config_RequestBody, db: Session = Depends(get_db)):

    config = Config(
        username=config_data.username,
        Monitoring_status=config_data.Monitoring_status,
        streaming_URL=config_data.streaming_URL,
        email=config_data.email,
    )
    
    db.add(config)
    db.commit()
    db.refresh(config)

    return (config)