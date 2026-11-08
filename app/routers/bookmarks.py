"""Bookmark endpoints – idempotent add/remove (P6-06)."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import crud, models
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(prefix="/api/me/bookmarks", tags=["bookmarks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BookmarkPayload(BaseModel):
    job_id: str


class BookmarkItem(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    category: str
    is_simulated: bool = False
    posted_at: Optional[datetime] = None
    saved_at: Optional[datetime] = None


class BookmarkListResponse(BaseModel):
    items: list[BookmarkItem]
    count: int
    next_offset: Optional[int] = None


class BookmarkCreateResponse(BookmarkItem):
    created: bool


def _to_item(bookmark: models.SavedJob) -> BookmarkItem:
    job = bookmark.job
    return BookmarkItem(
        job_id=bookmark.job_id,
        title=job.title if job else "Tanpa Judul",
        company=job.company if job else "Perusahaan",
        location=job.location if job else "Indonesia",
        category=job.category.name if (job and job.category) else "General",
        is_simulated=bool(job.is_simulated) if job else False,
        posted_at=job.posted_at if job else None,
        saved_at=bookmark.saved_at,
    )


@router.get("", response_model=BookmarkListResponse)
def list_bookmarks(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user),
):
    """Daftar lowongan yang disimpan pengguna."""
    bookmarks = crud.list_bookmarks(db, current.id, limit=limit, offset=offset)
    total = (
        db.query(models.SavedJob)
        .filter(models.SavedJob.user_id == current.id)
        .count()
    )
    next_offset = offset + limit if offset + limit < total else None
    return BookmarkListResponse(
        items=[_to_item(bookmark) for bookmark in bookmarks],
        count=total,
        next_offset=next_offset,
    )


@router.post("", response_model=BookmarkCreateResponse)
def add_bookmark(
    payload: BookmarkPayload,
    response: Response,
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user),
):
    """Simpan lowongan. Operasi idempotent (TC11)."""
    job = db.query(models.Job).filter(models.Job.id == payload.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lowongan tidak ditemukan",
        )

    existing = (
        db.query(models.SavedJob)
        .filter_by(user_id=current.id, job_id=payload.job_id)
        .first()
    )
    bookmark = crud.add_bookmark(db, current.id, payload.job_id)
    if existing is None:
        # Catat event save sekali saja; crud.log_event juga melakukan deduplikasi.
        crud.log_event(
            db,
            user_id=current.id,
            job_id=payload.job_id,
            event_type="save",
            is_simulated=False,
        )
        response.status_code = status.HTTP_201_CREATED

    return BookmarkCreateResponse(
        **_to_item(bookmark).model_dump(),
        created=existing is None,
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bookmark(
    job_id: str,
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user),
):
    """Hapus bookmark. Operasi idempotent (TC11)."""
    crud.remove_bookmark(db, current.id, job_id)
    return None
