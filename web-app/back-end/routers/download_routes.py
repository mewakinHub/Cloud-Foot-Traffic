from fastapi import FastAPI, HTTPException, Depends, APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Annotated, List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_db
import base64
import io
import zipfile

router = APIRouter()

@router.get("/{username}")
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
