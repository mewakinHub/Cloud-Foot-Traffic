from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Config

router = APIRouter()

class ConfigUpdateModel(BaseModel):
    streaming_URL: str
    email: str | None = None

@router.put("/config/{username}", response_model=ConfigUpdateModel)
def update_config(
    username: str, 
    update_data: ConfigUpdateModel, 
    db: Session = Depends(get_db)
):
    # Check if the user exists
    user = db.query(Config).filter(Config.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the fields dynamically
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    
    # Commit and refresh
    db.commit()
    db.refresh(user)
    return user