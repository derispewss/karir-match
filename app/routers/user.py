"""User‑related endpoints (delete user data) – Phase 6‑09."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, models
from ..routers.auth import get_current_user

router = APIRouter(prefix="/api/me", tags=["user"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete("/data", status_code=204)
def delete_my_data(db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):
    """Delete all personal data of the authenticated user (except evaluation data)."""
    crud.delete_user_data(db, current.id)
    return None
