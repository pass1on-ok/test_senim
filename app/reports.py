from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, auth
from .dependencies import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/", response_model=schemas.ReportOut)
def create_report(
    report: schemas.ReportCreate,
    current_user: models.User = Depends(get_current_user),  # <- тут
    db: Session = Depends(database.get_db)
):
    if not report.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    new_report = models.Report(**report.dict(), user_id=current_user.id)
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

@router.get("/", response_model=list[schemas.ReportOut])
def get_reports(
    current_user: models.User = Depends(get_current_user),  # <- тут
    db: Session = Depends(database.get_db)
):
    if current_user.role == "admin":
        return db.query(models.Report).all()
    return db.query(models.Report).filter(models.Report.user_id == current_user.id).all()