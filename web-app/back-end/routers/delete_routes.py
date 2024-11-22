from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Result, Config

router = APIRouter()

@router.delete("/result/{username}")
def delete_results(username:str, db: Session = Depends(get_db)):
    results_to_delete = db.query(Result).filter(Result.username == username)
    if results_to_delete.count() == 0:
        raise HTTPException(status_code=404, detail=f"No results found for username '{username}'")
    
    results_to_delete.delete(synchronize_session=False)
    db.commit()
    return {"message": f"All results for username '{username}' have been deleted."}

@router.delete("/config/{username}")
def delete_config(username:str, db: Session = Depends(get_db)):
    results_to_delete = db.query(Result).filter(Result.username == username)
    if results_to_delete.count() != 0:
        raise HTTPException(status_code=500, detail=f"Can't delete '{username}'")

    user_to_delete = db.query(Config).filter(Config.username == username)
    user_to_delete.delete(synchronize_session=False)
    db.commit()
    return {"message": f"'{username}' was deleted."}
