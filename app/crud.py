"""Repository layer – idempotent, seed, and parametrized queries (P6-02, P6-09)."""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from . import models
from datetime import datetime
import json


# ---------------- Users ----------------
def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(
    db: Session,
    *,
    email: str,
    hashed_password: str,
    full_name: Optional[str] = None,
    is_admin: bool = False
) -> models.User:
    user = models.User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        is_admin=is_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------------- Bookmarks (idempotent - TC11) ----------------
def add_bookmark(db: Session, user_id: int, job_id: str) -> models.SavedJob:
    existing = db.query(models.SavedJob).filter_by(user_id=user_id, job_id=job_id).first()
    if existing:
        return existing
    bookmark = models.SavedJob(user_id=user_id, job_id=job_id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def remove_bookmark(db: Session, user_id: int, job_id: str) -> None:
    obj = db.query(models.SavedJob).filter_by(user_id=user_id, job_id=job_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return None


def list_bookmarks(db: Session, user_id: int, limit: int = 100, offset: int = 0) -> List[models.SavedJob]:
    return (
        db.query(models.SavedJob)
        .filter_by(user_id=user_id)
        .order_by(models.SavedJob.saved_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


# ---------------- Preferences ----------------
def get_preferences(db: Session, user_id: int) -> Dict[str, Any]:
    pref = db.query(models.UserPreference).filter_by(user_id=user_id).first()
    return json.loads(pref.preferences_json) if pref else {}


def upsert_preferences(db: Session, user_id: int, preferences: Dict[str, Any]) -> models.UserPreference:
    pref = db.query(models.UserPreference).filter_by(user_id=user_id).first()
    json_blob = json.dumps(preferences, ensure_ascii=False)
    if pref:
        pref.preferences_json = json_blob
    else:
        pref = models.UserPreference(user_id=user_id, preferences_json=json_blob)
        db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref


# ---------------- Event tracking (dedup save - P6-07) ----------------
def log_event(
    db: Session,
    *,
    user_id: int,
    job_id: str,
    event_type: str,
    is_simulated: bool = False
) -> models.InteractionEvent:
    if event_type == "save":
        existing = (
            db.query(models.InteractionEvent)
            .filter_by(user_id=user_id, job_id=job_id, event_type="save")
            .first()
        )
        if existing:
            return existing
    ev = models.InteractionEvent(
        user_id=user_id,
        job_id=job_id,
        event_type=event_type,
        is_simulated=is_simulated,
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


# ---------------- Search History ----------------
def log_search(db: Session, user_id: int, query: str) -> models.SearchHistory:
    sh = models.SearchHistory(user_id=user_id, query=query)
    db.add(sh)
    db.commit()
    db.refresh(sh)
    return sh


# ---------------- Recommendation log ----------------
def log_recommendation(
    db: Session,
    *,
    user_id: int,
    job_id: str,
    source: str,
    rank: int
) -> models.RecommendationLog:
    rec = models.RecommendationLog(
        user_id=user_id,
        job_id=job_id,
        source=source,
        rank=rank,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


# ---------------- Delete User Data (P6-09) ----------------
def delete_user_data(db: Session, user_id: int) -> None:
    """Hapus preferensi, bookmark, riwayat pencarian, event, dan log rekomendasi

    dalam satu transaksi database. Data evaluasi TIDAK disentuh. Operasi idempoten.
    """
    with db.begin_nested():
        db.query(models.UserPreference).filter_by(user_id=user_id).delete()
        db.query(models.SavedJob).filter_by(user_id=user_id).delete()
        db.query(models.SearchHistory).filter_by(user_id=user_id).delete()
        db.query(models.InteractionEvent).filter_by(user_id=user_id).delete()
        db.query(models.RecommendationLog).filter_by(user_id=user_id).delete()
    db.commit()
