"""Interaction event tracking (P6-07)."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import crud, models
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(prefix="/api/events", tags=["events"])

EventType = Literal["view", "click", "save", "apply"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class EventPayload(BaseModel):
    job_id: str
    event_type: EventType
    is_simulated: bool = False


class EventResponse(BaseModel):
    event_id: int
    job_id: str
    event_type: EventType
    is_simulated: bool


@router.post("", response_model=EventResponse)
def create_event(
    payload: EventPayload,
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user),
):
    """Catat interaksi pengguna dengan lowongan."""
    job = db.query(models.Job).filter(models.Job.id == payload.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lowongan tidak ditemukan",
        )

    # Klien biasa tidak boleh menandai event sebagai simulasi.
    is_simulated = bool(payload.is_simulated and current.is_admin)
    event = crud.log_event(
        db,
        user_id=current.id,
        job_id=payload.job_id,
        event_type=payload.event_type,
        is_simulated=is_simulated,
    )
    return EventResponse(
        event_id=event.id,
        job_id=event.job_id,
        event_type=event.event_type,
        is_simulated=event.is_simulated,
    )
