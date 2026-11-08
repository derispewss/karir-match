"""Job search & detail endpoints – Phase 6-04.

Supports:
- Search by text query with TF-IDF cosine similarity.
- Filtering by category, location, and skills.
- Sorting by relevance (score) or date (posted_at).
- Limit and offset pagination.
- Empty states and 503 check when index is missing.
- Detail view for individual jobs.
"""

from pathlib import Path
from typing import List, Optional
from datetime import datetime
import sys

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, models

# Ensure research package is importable
sys.path.append(str(Path.cwd()))
import research.score as score

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search")
def search_jobs(
    q: Optional[str] = Query(None, description="Pencarian kata kunci"),
    category: Optional[str] = Query(None, description="Filter nama kategori"),
    location: Optional[str] = Query(None, description="Filter lokasi (misal: Jakarta, Remote)"),
    skill: Optional[str] = Query(None, description="Filter skill"),
    employment_type: Optional[str] = Query(None, description="Filter tipe pekerjaan"),
    experience_level: Optional[str] = Query(None, description="Filter level pengalaman"),
    sort: str = Query("score", pattern="^(score|date)$", description="Metode sorting: score atau date"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Pencarian lowongan kerja dengan integrasi TF-IDF dan filter metadata."""
    index_dir = Path("artifacts/tfidf_index")
    if not (index_dir / "manifest.json").exists():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Indeks pencarian belum siap. Harap jalankan pembuatan indeks terlebih dahulu.",
        )

    docs, field_vec = score.load_index(index_dir)
    cfg = score.load_config()
    weights = cfg.get("field_weights", {"title": 0.4, "skills": 0.3, "description": 0.3})

    # Jika ada kueri teks, lakukan skoring TF-IDF
    if q and q.strip():
        scored_pairs = score.rank_query(q.strip(), docs, field_vec, weights, top_k=len(docs))
        score_map = {doc_id: s for doc_id, s in scored_pairs}
    else:
        score_map = {d["id"]: 0.0 for d in docs}

    # Bangun peta dokumen dari index
    doc_map = {d["id"]: d for d in docs}

    # Ambil metadata tambahan dari database (category, posted_at, skills)
    db_jobs = {j.id: j for j in db.query(models.Job).all()}

    # Terapkan filter
    filtered_ids = []
    for doc_id, d in doc_map.items():
        if q and q.strip() and score_map.get(doc_id, 0.0) <= 0.0:
            continue
        db_job = db_jobs.get(doc_id)
        if db_job is not None and not db_job.is_active:
            continue
        # Filter kategori
        if category and db_job:
            cat_name = db_job.category.name if db_job.category else ""
            if category.lower() not in cat_name.lower():
                continue
        # Filter lokasi
        if location:
            doc_loc = d.get("location", "")
            if db_job and db_job.location:
                doc_loc = db_job.location
            if location.lower() not in doc_loc.lower():
                continue
        # Filter skill
        if skill:
            doc_skills = d.get("skills", "")
            if db_job and db_job.skills:
                doc_skills += " " + " ".join(s.name for s in db_job.skills)
            if skill.lower() not in doc_skills.lower():
                continue
        # Filter tipe pekerjaan
        if employment_type:
            doc_type = d.get("employment_type", "")
            if db_job and db_job.employment_type:
                doc_type = db_job.employment_type
            if employment_type.lower() not in str(doc_type).lower():
                continue
        # Filter level pengalaman
        if experience_level:
            doc_level = d.get("experience_level", "")
            if db_job and db_job.experience_level:
                doc_level = db_job.experience_level
            if experience_level.lower() not in str(doc_level).lower():
                continue

        filtered_ids.append(doc_id)

    # Lakukan sorting
    if sort == "date":
        def get_date(did):
            job = db_jobs.get(did)
            return job.posted_at if (job and job.posted_at) else datetime.min
        filtered_ids.sort(key=lambda did: (get_date(did), score_map.get(did, 0.0), did), reverse=True)
    else:
        # Default sort: score descending, then doc_id ascending
        filtered_ids.sort(key=lambda did: (-score_map.get(did, 0.0), did))

    total = len(filtered_ids)
    sliced = filtered_ids[offset : offset + limit]

    results = []
    for rank, doc_id in enumerate(sliced, start=1 + offset):
        d = doc_map.get(doc_id, {})
        db_job = db_jobs.get(doc_id)
        sc = score_map.get(doc_id, 0.0)

        # match_level interpretatif tanpa membocorkan skor mentah
        if sc > 0.4:
            match_level = "Sangat Sesuai"
        elif sc > 0.15:
            match_level = "Sesuai"
        elif sc > 0.0:
            match_level = "Cukup Sesuai"
        else:
            match_level = "Standar"

        haystack = " ".join(
            [
                str(d.get("title", "")),
                str(d.get("skills", "")),
                str(d.get("description", "")),
                db_job.company if db_job else "",
            ]
        ).lower()
        matched_terms = list(
            dict.fromkeys(
                term
                for term in (q.split() if q else [])
                if term.lower() in haystack
            )
        )
        if matched_terms:
            reason = "Cocok pada istilah: " + ", ".join(matched_terms) + "."
        elif q:
            reason = "Lowongan relevan berdasarkan kemiripan teks dengan kueri."
        else:
            reason = "Lowongan terbaru tanpa skor kueri teks."

        results.append({
            "job_id": doc_id,
            "title": d.get("title", db_job.title if db_job else "Tanpa Judul"),
            "company": d.get("company", db_job.company if db_job else "Perusahaan"),
            "location": d.get("location", db_job.location if db_job else "Indonesia"),
            "category": db_job.category.name if (db_job and db_job.category) else "General",
            "employment_type": (
                db_job.employment_type if db_job else d.get("employment_type")
            ),
            "experience_level": (
                db_job.experience_level if db_job else d.get("experience_level")
            ),
            "is_simulated": bool(db_job.is_simulated) if db_job else bool(d.get("is_simulated")),
            "match_level": match_level,
            "matched_terms": matched_terms,
            "reason": reason,
            "posted_at": db_job.posted_at.isoformat() if (db_job and db_job.posted_at) else None,
        })

    payload = {
        "query": q or "",
        "total": total,
        "limit": limit,
        "offset": offset,
        "sort": sort,
        "results": results,
    }
    if total == 0:
        payload["message"] = (
            "Tidak ada lowongan yang cocok. Coba ubah kata kunci atau filter."
        )
    return payload


@router.get("/{job_id}")
def get_job_detail(job_id: str, db: Session = Depends(get_db)):
    """Detail lengkap lowongan kerja."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Lowongan tidak ditemukan")

    return {
        "job_id": job.id,
        "title": job.title,
        "description": job.description,
        "company": job.company,
        "location": job.location,
        "category": job.category.name if job.category else None,
        "employment_type": job.employment_type,
        "experience_level": job.experience_level,
        "source": job.source,
        "is_active": job.is_active,
        "is_simulated": job.is_simulated,
        "skills": [s.name for s in job.skills],
        "posted_at": job.posted_at.isoformat() if job.posted_at else None,
    }
