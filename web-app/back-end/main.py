from fastapi import FastAPI, HTTPException, Depends, APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Annotated, List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
import io
import zipfile


app = FastAPI()
router = APIRouter()
models.Base.metadata.create_all(bind=engine)

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for the request body
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
    processed_detection_image: str

class ResultCreateModel(BaseModel):
    username: str
    config: str | None = None
    result: int
    image_url: str  # URL to the PNG image

class StreamingURLUpdateModel(BaseModel):
    streaming_URL: str

class EmailUpdateModel(BaseModel):
    email: str

db_dependency = Annotated[Session, Depends(get_db)]

@app.put("/edit/{username}", response_model=ConfigModel)
def update_streaming_url(username: str, update_data: StreamingURLUpdateModel, db: db_dependency):
    # Check if the username exists
    user = db.query(models.Config).filter(models.Config.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the `streaming_URL` field
    user.streaming_URL = update_data.streaming_URL
    
    db.commit()
    db.refresh(user)
    return user

@app.get("/configs", response_model=List[ConfigModel])
def get_all_configs(db: Session = Depends(get_db)):
    # Query all records from the Config table
    configs = db.query(models.Config).all()
    return configs

@app.put("/email/{username}", response_model=ConfigModel)
def update_email(username: str, update_data: EmailUpdateModel, db: db_dependency):
    # Check if the username exists
    user = db.query(models.Config).filter(models.Config.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the `email` field
    user.email = update_data.email
    
    db.commit()
    db.refresh(user)
    return user

@app.post("/results")
def create_result(result_data: ResultCreateModel, db: Session = Depends(get_db)):
    # Fetch the image from the provided URL
    try:
        response = requests.get(result_data.image_url)
        response.raise_for_status()
        if "image/png" not in response.headers["Content-Type"]:
            raise HTTPException(status_code=400, detail="Provided URL does not contain a valid PNG image")
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image: {str(e)}")

    # Convert the image to Base64
    try:
        image_base64 = base64.b64encode(response.content).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    # Fetch the current timestamp
    current_time = datetime.now()

    # Create a new Result record
    new_result = models.Result(
        username=result_data.username,
        DATE_TIME=current_time,  # Automatically set the current time
        config=result_data.config,
        result=result_data.result,
        processed_detection_image=image_base64,
    )

    # Insert into the database
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return {"message": "Result created successfully", "result_id": new_result.result_id}

@app.delete("/results/{username}")
def delete_results(username: str, db: Session = Depends(get_db)):
    # Query for all rows with the specified username
    results_to_delete = db.query(models.Result).filter(models.Result.username == username)

    # Check if any rows exist for the username
    if results_to_delete.count() == 0:
        raise HTTPException(status_code=404, detail=f"No results found for username '{username}'")

    # Delete the rows
    results_to_delete.delete(synchronize_session=False)
    db.commit()

    return {"message": f"All results for username '{username}' have been deleted."}

@router.get("/download_image/{username}")
def download_images(username: str, db: Session = Depends(get_db)):
    # Query all rows matching the username
    results = db.query(models.Result).filter(models.Result.username == username).all()
    
    if not results:
        raise HTTPException(status_code=404, detail=f"No results found for username '{username}'")

    # Create an in-memory byte stream for the ZIP file
    zip_buffer = io.BytesIO()

    # Create the ZIP file in memory
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for result in results:
            if result.processed_detection_image:
                try:
                    # Decode Base64 image data
                    image_data = base64.b64decode(result.processed_detection_image)

                    # Define the filename for the image (you can customize this logic)
                    filename = f"image_{result.result_id}.png"
                    
                    # Write the image data to the zip file
                    zip_file.writestr(filename, image_data)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error processing image {result.result_id}: {str(e)}")

    # Seek to the beginning of the BytesIO buffer
    zip_buffer.seek(0)

    # Return the ZIP file as a downloadable file
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        "Content-Disposition": "attachment; filename=images.zip"
    })

app.include_router(router)
