"""User preferences endpoints – Phase 6-05."""

from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, models
from .auth import get_current_user

router = APIRouter(prefix="/api/me/preferences", tags=["preferences"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PreferencesPayload(BaseModel):
    categories: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    employment_types: List[str] = Field(default_factory=list)
    experience_levels: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


class PreferencesResponse(BaseModel):
    user_id: int
    preferences: PreferencesPayload


@router.get("", response_model=PreferencesResponse)
def read_preferences(
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user),
):
    """Ambil preferensi pengguna terautentikasi."""
    prefs = crud.get_preferences(db, current.id)
    return PreferencesResponse(
        user_id=current.id,
        preferences=PreferencesPayload.model_validate(prefs),
    )


@router.put("", response_model=PreferencesResponse)
def update_preferences(
    payload: PreferencesPayload,
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user),
):
    """Perbarui preferensi pengguna terautentikasi."""
    prefs = payload.model_dump()
    crud.upsert_preferences(db, current.id, prefs)
    return PreferencesResponse(user_id=current.id, preferences=payload)
