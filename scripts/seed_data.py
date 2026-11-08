"""Seed script – idempotent (P6-02)."""

import json
import sys
from pathlib import Path

# Pastikan root proyek dapat diimpor saat script dijalankan langsung.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app import crud, models

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEFAULT_CATEGORIES = ["Software Engineering", "Data Science", "Product Management"]
DEFAULT_SKILLS = ["python", "fastapi", "react", "nodejs", "sql", "tableau"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_corpus() -> list[dict]:
    corpus_path = Path("data/processed/corpus_id_v1.json")
    if not corpus_path.exists():
        print("Corpus not found – skip job seeding")
        return []
    return load_json(corpus_path)


def corpus_categories(docs: list[dict]) -> list[str]:
    names = {
        str(doc["job_category"]).strip()
        for doc in docs
        if doc.get("job_category")
    }
    return sorted(names)


def corpus_skills(docs: list[dict]) -> list[str]:
    names: set[str] = set()
    for doc in docs:
        raw = doc.get("skills", "")
        if isinstance(raw, str):
            names.update(part.strip().lower() for part in raw.split() if part.strip())
    return sorted(names)


def seed_categories(db: Session, names: list[str]):
    for name in names:
        if not db.query(models.JobCategory).filter_by(name=name).first():
            db.add(models.JobCategory(name=name))
    db.commit()


def seed_skills(db: Session, names: list[str]):
    for name in names:
        if not db.query(models.Skill).filter_by(name=name).first():
            db.add(models.Skill(name=name))
    db.commit()


def seed_jobs(db: Session, docs: list[dict]):
    categories = {c.name: c for c in db.query(models.JobCategory).all()}
    skills = {s.name: s for s in db.query(models.Skill).all()}

    for doc in docs:
        job = db.query(models.Job).filter_by(id=doc["id"]).first()
        if not job:
            job = models.Job(
                id=doc["id"],
                title=doc.get("title", "tanpa judul"),
                description=doc.get("description", ""),
                company=doc.get("company", "unknown"),
                location=doc.get("location", "unknown"),
            )
            db.add(job)

        job.employment_type = doc.get("employment_type") or job.employment_type
        job.experience_level = doc.get("experience_level") or job.experience_level
        job.source = doc.get("source") or "corpus_id_v1"
        job.is_active = bool(doc.get("is_active", True))
        job.is_simulated = bool(doc.get("is_simulated", False))

        category_name = str(doc.get("job_category", "")).strip()
        if category_name:
            job.category = categories.get(category_name)

        raw_skills = doc.get("skills", "")
        if isinstance(raw_skills, str):
            skill_names = {
                part.strip().lower() for part in raw_skills.split() if part.strip()
            }
            job.skills = [skills[name] for name in sorted(skill_names) if name in skills]

    db.commit()


def seed_admin(db: Session):
    admin_email = "admin@example.com"
    if not crud.get_user_by_email(db, admin_email):
        hashed = pwd_ctx.hash("AdminPass123!")
        crud.create_user(
            db,
            email=admin_email,
            hashed_password=hashed,
            full_name="Admin User",
            is_admin=True,
        )
    db.commit()


def main():
    Base.metadata.create_all(bind=engine)
    docs = load_corpus()
    db = SessionLocal()
    try:
        seed_categories(
            db,
            sorted(set(DEFAULT_CATEGORIES) | set(corpus_categories(docs))),
        )
        seed_skills(
            db,
            sorted(set(DEFAULT_SKILLS) | set(corpus_skills(docs))),
        )
        seed_jobs(db, docs)
        seed_admin(db)
        print("✅ Seed data selesai – idempotent")
    finally:
        db.close()


if __name__ == "__main__":
    main()
