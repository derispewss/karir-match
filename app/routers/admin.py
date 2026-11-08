"""Admin evaluation endpoints (P6-10)."""

from datetime import datetime
from pathlib import Path
import hashlib
import subprocess
import sys

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from .. import models
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(prefix="/api/admin/eval", tags=["admin"])

CONFIG_PATH = Path("config/preprocess.yaml")
DATASET_PATH = Path("data/processed/corpus_id_v1.json")


def _sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_admin(
    request: Request,
    db: Session = Depends(get_db),
) -> models.User:
    user = get_current_user(request, db)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only",
        )
    return user


@router.get("/summary")
def eval_summary(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    """Ringkasan artefak evaluasi yang tersimpan di database."""
    return {
        "queries": db.query(models.EvalQuery).count(),
        "judgments": db.query(models.RelevanceJudgment).count(),
        "runs": db.query(models.EvalRun).count(),
        "config_hash": _sha256_file(CONFIG_PATH),
        "dataset_hash": _sha256_file(DATASET_PATH),
    }


@router.post("/run")
def trigger_eval(
    config_path: str = Query("artifacts", description="Direktori run evaluasi"),
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    """Jalankan evaluasi dan simpan catatan run."""
    allowed_root = Path("artifacts").resolve()
    target = Path(config_path).resolve()

    if not str(target).startswith(str(allowed_root)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Path harus berada di dalam folder artifacts",
        )

    if not target.exists():
        target = allowed_root

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    report_path = allowed_root / f"evaluation_report_{timestamp}.md"
    command = [
        sys.executable,
        "research/evaluate_runs.py",
        "--run-dir",
        str(target),
        "--out",
        str(report_path),
    ]

    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode != 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluasi gagal: {process.stderr.strip() or process.stdout.strip()}",
        )

    run = models.EvalRun(
        run_name=f"run_{timestamp}",
        run_path=str(report_path),
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    return {
        "detail": "Evaluation triggered",
        "run_id": run.id,
        "report_path": str(report_path),
        "config_hash": _sha256_file(CONFIG_PATH),
        "dataset_hash": _sha256_file(DATASET_PATH),
    }
