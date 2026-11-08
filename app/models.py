"""ORM schema – Phase 6 (P6-01)."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime, Enum, ForeignKey,
    Index, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from .database import Base

# ---------------- Users ----------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    saved_jobs = relationship("SavedJob", back_populates="user", cascade="all, delete-orphan")
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
    events = relationship("InteractionEvent", back_populates="user", cascade="all, delete-orphan")
    recommendation_logs = relationship("RecommendationLog", back_populates="user", cascade="all, delete-orphan")


# ---------------- Job taxonomy ----------------
class JobCategory(Base):
    __tablename__ = "job_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True)               # job_id from dataset
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    employment_type = Column(String, nullable=True)
    experience_level = Column(String, nullable=True)
    source = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_simulated = Column(Boolean, nullable=False, default=False)
    posted_at = Column(DateTime, default=datetime.utcnow)

    category_id = Column(Integer, ForeignKey("job_categories.id", ondelete="SET NULL"), nullable=True)
    category = relationship("JobCategory", backref="jobs")

    skills = relationship(
        "Skill",
        secondary="job_skills",
        backref="jobs",
    )

    __table_args__ = (
        Index("ix_jobs_location", "location"),
        Index("ix_jobs_category_id", "category_id"),
        Index("ix_jobs_employment_type", "employment_type"),
        Index("ix_jobs_experience_level", "experience_level"),
        Index("ix_jobs_active_posted", "is_active", "posted_at"),
    )


class JobSkill(Base):
    __tablename__ = "job_skills"
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)


# ---------------- User artefacts ----------------
class UserPreference(Base):
    __tablename__ = "user_preferences"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    preferences_json = Column(Text, nullable=False, default="{}")
    user = relationship("User", back_populates="preferences")


class SavedJob(Base):
    """Bookmark – idempotent (TC11)."""
    __tablename__ = "saved_jobs"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True)
    saved_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saved_jobs")
    job = relationship("Job")

    __table_args__ = (
        Index("ix_saved_jobs_user_saved", "user_id", "saved_at"),
    )


class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    query = Column(String, nullable=False)
    performed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="search_history")

    __table_args__ = (
        Index("ix_search_history_user_performed", "user_id", "performed_at"),
    )


class InteractionEvent(Base):
    __tablename__ = "interaction_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"))
    event_type = Column(
        Enum("view", "click", "save", "apply", name="event_type_enum"),
        nullable=False,
    )
    is_simulated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="events")
    job = relationship("Job")

    __table_args__ = (
        Index("ix_events_user_created", "user_id", "created_at"),
        Index("ix_events_job_type", "job_id", "event_type"),
        Index("ix_events_simulated", "is_simulated"),
    )


class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"))
    source = Column(String, nullable=False)   # tfidf / profile
    rank = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendation_logs")
    job = relationship("Job")

    __table_args__ = (
        Index("ix_rec_logs_user_created", "user_id", "created_at"),
    )


# ---------------- Evaluation artefacts ----------------
class EvalQuery(Base):
    __tablename__ = "eval_queries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_id = Column(String, unique=True, nullable=False)
    query_text = Column(String, nullable=False)


class RelevanceJudgment(Base):
    __tablename__ = "relevance_judgments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_id = Column(String, nullable=False, index=True)
    doc_id = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)   # 0-2
    __table_args__ = (
        CheckConstraint("grade BETWEEN 0 AND 2", name="ck_judgment_grade_0_2"),
        UniqueConstraint("query_id", "doc_id", name="uq_judgment_qd"),
    )


class EvalRun(Base):
    __tablename__ = "eval_runs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_name = Column(String, nullable=False)
    run_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
