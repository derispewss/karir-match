"""Personalized recommendation feed (P6-08).

Uses the user's saved preferences as a TF-IDF query when available and falls
back to the latest jobs. Bookmarked jobs are excluded from the feed.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional
import sys

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import crud, models
from ..database import SessionLocal
from .auth import get_current_user

# Ensure the research package is importable when running from the project root.
sys.path.append(str(Path.cwd()))
import research.score as score  # noqa: E402

router = APIRouter(prefix="/api/me/recommendations", tags=["recommendations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RecommendationItem(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    category: str
    match_level: str
    source: str
    reason: str
    is_simulated: bool = False
    posted_at: Optional[str] = None


class RecommendationResponse(BaseModel):
    results: list[RecommendationItem]


def _match_level(value: float) -> str:
    if value > 0.4:
        return "Sangat Sesuai"
    if value > 0.15:
        return "Sesuai"
    if value > 0.0:
        return "Cukup Sesuai"
    return "Standar"


def _preference_query(preferences: dict) -> str:
    """Build a text query from a flexible preferences JSON object."""
    parts: list[str] = []
    for key in ("query", "keywords", "job_titles", "skills", "categories", "locations"):
        value = preferences.get(key)
        if isinstance(value, list):
            parts.extend(str(item) for item in value if str(item).strip())
        elif isinstance(value, str) and value.strip():
            parts.append(value.strip())
    return " ".join(parts).strip()


@router.get("", response_model=RecommendationResponse)
def get_recommendations(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user),
):
    """Rekomendasi lowongan yang dipersonalisasi untuk pengguna."""
    preferences = crud.get_preferences(db, current.id)
    query_text = _preference_query(preferences) if isinstance(preferences, dict) else ""

    bookmarked_ids = {
        bookmark.job_id
        for bookmark in crud.list_bookmarks(db, current.id, limit=1000)
    }
    db_jobs = {job.id: job for job in db.query(models.Job).all()}

    ranked_ids: list[str] = []
    score_map: dict[str, float] = {}
    source = "latest"

    index_dir = Path("artifacts/tfidf_index")
    if query_text and (index_dir / "manifest.json").exists():
        try:
            docs, field_vec = score.load_index(index_dir)
            config = score.load_config()
            weights = config.get(
                "field_weights",
                {"title": 0.4, "skills": 0.3, "description": 0.3},
            )
            scored_pairs = score.rank_query(
                query_text,
                docs,
                field_vec,
                weights,
                top_k=len(docs),
            )
            for doc_id, value in scored_pairs:
                if value <= 0.0:
                    continue
                if doc_id in bookmarked_ids or doc_id not in db_jobs:
                    continue
                if not db_jobs[doc_id].is_active:
                    continue
                ranked_ids.append(doc_id)
                score_map[doc_id] = float(value)
                if len(ranked_ids) >= limit:
                    break
            if ranked_ids:
                source = "profile"
        except Exception:
            # Fall back to latest jobs if the index cannot be loaded.
            ranked_ids = []
            score_map = {}

    if not ranked_ids:
        candidates = [
            job
            for job_id, job in db_jobs.items()
            if job_id not in bookmarked_ids and job.is_active
        ]
        candidates.sort(
            key=lambda job: (
                job.posted_at is not None,
                job.posted_at or datetime.min,
                job.id,
            ),
            reverse=True,
        )
        ranked_ids = [job.id for job in candidates[:limit]]

    results: list[RecommendationItem] = []
    for rank, job_id in enumerate(ranked_ids, start=1):
        job = db_jobs.get(job_id)
        if not job:
            continue

        if source == "profile":
            reason = "Dipersonalisasi dari preferensi dan profil Anda."
        else:
            reason = "Lowongan terbaru; lengkapi preferensi untuk personalisasi."

        results.append(
            RecommendationItem(
                job_id=job.id,
                title=job.title,
                company=job.company,
                location=job.location,
                category=job.category.name if job.category else "General",
                match_level=_match_level(score_map.get(job_id, 0.0)),
                source=source,
                reason=reason,
                is_simulated=job.is_simulated,
                posted_at=job.posted_at.isoformat() if job.posted_at else None,
            )
        )

        try:
            crud.log_recommendation(
                db,
                user_id=current.id,
                job_id=job.id,
                source=source,
                rank=rank,
            )
        except Exception:
            # Recommendation logging should not break the feed.
            pass

    return RecommendationResponse(results=results)
